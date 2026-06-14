#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path

PACKAGE_ROOT = Path.home() / "Projects" / "pkg-sources" / "os" / "1-lts"
REPO_ROOT = Path.home() / "Projects" / "anysolo-test" / "repo" / "1-lts"
BUILD_ONLY = {"autoconf", "automake", "binutils", "bison", "cmake", "dejagnu", "flex", "gawk", "gcc", "gettext", "gperf", "help2man", "make", "meson", "ninja", "pkgconf", "texinfo"}


@dataclass(frozen=True)
class Package:
    name: str
    version: str
    arch: str
    path: Path
    depends: tuple[str, ...]
    comment: str
    has_build: bool
    sources: tuple[Path, ...]
    dist: tuple[Path, ...]


def clean(v: str) -> str:
    v = v.strip()
    return v[1:-1] if len(v) > 1 and v[0] == v[-1] and v[0] in "'\"" else v


def parse_yml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current = None
    for raw in path.read_text(errors="replace").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if current and s.startswith("- "):
            data.setdefault(current, [])
            data[current].append(clean(s[2:]))
            continue
        if not raw.startswith((" ", "\t")):
            current = None
        if ":" not in s:
            continue
        key, value = s.split(":", 1)
        key, value = key.strip(), value.strip()
        if value == "[]":
            data[key] = []
        elif value:
            data[key] = clean(value)
        else:
            data[key] = []
            current = key
    return data


def archives(path: Path, patterns: tuple[str, ...]) -> tuple[Path, ...]:
    out = []
    for pattern in patterns:
        out.extend(path.glob(pattern))
    return tuple(sorted(p for p in out if p.is_file()))


def repo_archives(repo_root: Path, pkg: str) -> tuple[Path, ...]:
    root = repo_root / pkg
    if not root.exists():
        return ()
    return archives(root, ("*/*.txpk.tar.bz2", "*/*.txpk.tar.gz", "*/*.txpk.tar.xz"))


def load(root: Path) -> dict[str, Package]:
    packages = {}
    for package_yml in sorted(root.glob("*/package.yml")):
        package_dir = package_yml.parent
        meta = parse_yml(package_yml)
        name = str(meta.get("name") or package_dir.name)
        src = package_dir / "src"
        dist = package_dir / "dist"
        packages[name] = Package(
            name=name,
            version=str(meta.get("version") or ""),
            arch=str(meta.get("arch") or ""),
            path=package_dir,
            depends=tuple(str(d) for d in meta.get("depends", []) if str(d)),
            comment=str(meta.get("comment") or ""),
            has_build=(package_dir / "build.sh").is_file(),
            sources=tuple(sorted(p for p in src.iterdir() if p.is_file())) if src.exists() else (),
            dist=archives(dist, ("*.txpk.tar.bz2", "*.txpk.tar.gz", "*.txpk.tar.xz")) if dist.exists() else (),
        )
    return packages


def reverse(packages):
    rev = {name: set() for name in packages}
    for p in packages.values():
        for dep in p.depends:
            rev.setdefault(dep, set()).add(p.name)
    return rev


def transitive(packages, name):
    seen, stack = set(), list(packages.get(name, Package(name, "", "", Path(), (), "", False, (), ())).depends)
    while stack:
        dep = stack.pop()
        if dep in seen:
            continue
        seen.add(dep)
        if dep in packages:
            stack.extend(packages[dep].depends)
    return seen


def path_to(packages, start, target):
    queue, seen = [(start, [start])], {start}
    while queue:
        cur, path = queue.pop(0)
        for dep in packages.get(cur, Package(cur, "", "", Path(), (), "", False, (), ())).depends:
            if dep == target:
                return path + [target]
            if dep not in seen:
                seen.add(dep)
                queue.append((dep, path + [dep]))
    return None


def node(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", name)


def summary(packages, repo_root):
    built = sum(1 for p in packages.values() if p.dist or repo_archives(repo_root, p.name))
    print(f"packages: {len(packages)}")
    print(f"built artifacts present: {built}")
    print(f"unbuilt/no dist archive: {len(packages) - built}")


def lint(packages):
    known = set(packages)
    errors = warnings = 0
    for p in sorted(packages.values(), key=lambda x: x.name):
        def issue(level, msg):
            nonlocal errors, warnings
            errors += level == "error"
            warnings += level == "warning"
            print(f"{level}: {p.name}: {msg}")
        if not p.version or not re.fullmatch(r"[0-9][0-9A-Za-z.+_~-]*", p.version):
            issue("error", f"bad or missing version: {p.version}")
        if not p.comment:
            issue("warning", "missing practical comment field")
        if not p.has_build:
            issue("error", "missing build.sh")
        if not p.sources:
            issue("warning", "missing source archive in src/")
        build = p.path / "build.sh"
        if build.exists():
            text = build.read_text(errors="replace")
            if re.search(r"(^|\s)(make|ninja)\s+install(\s|$)", text) and "DESTDIR" not in text:
                issue("error", "build.sh appears to install without DESTDIR")
            if "TXPK_PACKAGE_BUILD_DIST_DIR" not in text:
                issue("warning", "build.sh does not mention TXPK_PACKAGE_BUILD_DIST_DIR")
        if (p.path / "dist").exists():
            issue("warning", "generated dist/ directory is present")
        for dep in p.depends:
            if dep not in known:
                issue("warning", f"depends on unknown package: {dep}")
            if dep in BUILD_ONLY:
                issue("warning", f"runtime deps include likely build-only tool: {dep}")
    print(f"lint: {errors} errors, {warnings} warnings")
    return 1 if errors else 0


def write_graph(packages, output: Path, report: Path):
    lines = ["flowchart LR"]
    for p in sorted(packages.values(), key=lambda x: x.name):
        if not p.depends:
            lines.append(f'  {node(p.name)}["{p.name}"]')
        for dep in sorted(p.depends):
            lines.append(f'  {node(p.name)}["{p.name}"] --> {node(dep)}["{dep}"]')
    output.write_text("\n".join(lines) + "\n")
    direct = sorted(n for n, p in packages.items() if "systemd" in p.depends)
    trans = sorted(n for n in packages if "systemd" in transitive(packages, n))
    body = ["# Tuxenix Dependency Report", "", f"Packages scanned: {len(packages)}", f"Direct systemd deps: {len(direct)}", f"Transitive systemd deps: {len(trans)}", "", "## Direct systemd dependencies", ""]
    body += [f"- {n}" for n in direct]
    body += ["", "## Transitive systemd paths", ""]
    for n in trans:
        p = path_to(packages, n, "systemd")
        if p:
            body.append(f"- {' -> '.join(p)}")
    report.write_text("\n".join(body) + "\n")
    print(f"wrote {output}")
    print(f"wrote {report}")


def write_explorer(packages, output: Path):
    rev = reverse(packages)
    rows = []
    for p in sorted(packages.values(), key=lambda x: x.name):
        deps = " ".join(html.escape(d) for d in p.depends) or "none"
        rdeps = " ".join(html.escape(d) for d in sorted(rev.get(p.name, []))) or "none"
        rows.append(f"<tr><td><b>{html.escape(p.name)}</b></td><td>{html.escape(p.version)}</td><td>{deps}</td><td>{rdeps}</td><td>{html.escape(p.comment)}</td></tr>")
    output.write_text(f"""<!doctype html><meta charset=utf-8><title>Tuxenix Package Explorer</title><style>body{{font-family:system-ui;margin:24px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:8px;vertical-align:top}}th{{background:#eee}}input{{padding:10px;width:420px}}</style><h1>Tuxenix Package Explorer</h1><p>{len(packages)} package recipes indexed.</p><input id=q placeholder='search'><table><thead><tr><th>Package</th><th>Version</th><th>Deps</th><th>Reverse deps</th><th>Comment</th></tr></thead><tbody>{''.join(rows)}</tbody></table><script>q.oninput=()=>document.querySelectorAll('tbody tr').forEach(r=>r.style.display=r.innerText.toLowerCase().includes(q.value.toLowerCase())?'':'none')</script>""")
    print(f"wrote {output}")


def write_dashboard(packages, output: Path, repo_root: Path):
    rows, built = [], 0
    for p in sorted(packages.values(), key=lambda x: x.name):
        arts = p.dist or repo_archives(repo_root, p.name)
        built += bool(arts)
        status = "built" if arts else "missing"
        src = ", ".join(x.name for x in p.sources) or "missing"
        dist = ", ".join(x.name for x in arts) or "missing"
        rows.append(f"<tr><td><b>{html.escape(p.name)}</b></td><td>{html.escape(p.version)}</td><td>{status}</td><td>{html.escape(src)}</td><td>{html.escape(dist)}</td></tr>")
    output.write_text(f"""<!doctype html><meta charset=utf-8><title>Tuxenix Build Dashboard</title><style>body{{font-family:system-ui;margin:24px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:8px}}th{{background:#eee}}</style><h1>Tuxenix Build Dashboard</h1><p>Packages: {len(packages)} | Built artifacts: {built} | Missing: {len(packages)-built}</p><table><thead><tr><th>Package</th><th>Version</th><th>Status</th><th>Sources</th><th>Artifacts</th></tr></thead><tbody>{''.join(rows)}</tbody></table>""")
    print(f"wrote {output}")


def vm(action, workspace: Path, kernel_version: str):
    image = workspace / "tuxenix.img"
    if action in {"boot", "serial"}:
        display = "none" if action == "serial" else "gtk"
        print(f"cd {workspace}\nqemu-system-x86_64 \\\n  -enable-kvm \\\n  -m 4096 \\\n  -smp 4 \\\n  -cpu host \\\n  -drive file={image.name},format=raw,if=virtio \\\n  -kernel /boot/vmlinuz-linux \\\n  -initrd /boot/initramfs-linux.img \\\n  -append \"root=/dev/vda1 rw init=/usr/lib/systemd/systemd systemd.unit=multi-user.target console=ttyS0\" \\\n  -device virtio-vga \\\n  -netdev user,id=net0 \\\n  -device virtio-net-pci,netdev=net0 \\\n  -display {display} \\\n  -serial mon:stdio")
    elif action == "inject-modules":
        version = kernel_version or "$(uname -r)"
        print(f"sudo env TMPDIR=/tmp LIBGUESTFS_CACHEDIR=/tmp/guestfs-cache XDG_RUNTIME_DIR=/tmp/runtime-elgun virt-copy-in -a {image} -m /dev/sda1 /usr/lib/modules/{version} /usr/lib/modules")
    elif action == "snapshot":
        print(f"cp -av {image} {workspace}/tuxenix-$(date +%Y%m%d-%H%M%S).img")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", type=Path, default=PACKAGE_ROOT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summary").add_argument("--repo-root", type=Path, default=REPO_ROOT)
    sub.add_parser("lint")
    g = sub.add_parser("graph"); g.add_argument("--output", type=Path, default=Path("deps.mmd")); g.add_argument("--systemd-report", type=Path, default=Path("systemd-report.md"))
    e = sub.add_parser("explorer"); e.add_argument("--output", type=Path, default=Path("package-explorer.html"))
    d = sub.add_parser("dashboard"); d.add_argument("--output", type=Path, default=Path("build-dashboard.html")); d.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    v = sub.add_parser("vm"); v.add_argument("action", choices=["boot", "serial", "inject-modules", "snapshot"]); v.add_argument("--workspace", type=Path, default=Path.home() / "Projects" / "anysolo-test"); v.add_argument("--kernel-version", default="")
    args = ap.parse_args()
    if args.cmd == "vm":
        vm(args.action, args.workspace, args.kernel_version); return 0
    packages = load(args.package_root)
    if args.cmd == "summary": summary(packages, args.repo_root); return 0
    if args.cmd == "lint": return lint(packages)
    if args.cmd == "graph": write_graph(packages, args.output, args.systemd_report); return 0
    if args.cmd == "explorer": write_explorer(packages, args.output); return 0
    if args.cmd == "dashboard": write_dashboard(packages, args.output, args.repo_root); return 0


if __name__ == "__main__":
    raise SystemExit(main())

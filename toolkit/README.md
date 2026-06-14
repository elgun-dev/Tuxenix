# Tuxenix Toolkit

A practical toolkit for Tuxenix package work, dependency analysis, build visibility, and QEMU boot testing.

This folder contains the first six GitHub-facing project ideas in one usable tool:

1. Package recipe linter
2. Dependency graph generator
3. Package explorer
4. Build dashboard
5. LFS/Tuxenix boot lab notes
6. Tuxenix VM launcher/helper

The local development repo is:

```text
~/Projects/tuxenix-toolkit
```

## Quick Start

```sh
python3 tuxenix_toolkit.py summary
python3 tuxenix_toolkit.py lint
python3 tuxenix_toolkit.py graph --output deps.mmd --systemd-report systemd-report.md
python3 tuxenix_toolkit.py explorer --output package-explorer.html
python3 tuxenix_toolkit.py dashboard --output build-dashboard.html
python3 tuxenix_toolkit.py vm boot
```

By default the tool reads package recipes from:

```text
~/Projects/pkg-sources/os/1-lts
```

and package artifacts from:

```text
~/Projects/anysolo-test/repo/1-lts
```

## Highlights

- Scans `package.yml`, `build.sh`, `src/`, and package artifact locations.
- Reports missing comments, bad versions, missing source archives, and risky install commands.
- Generates a Mermaid dependency graph.
- Reports direct and transitive `systemd` dependency paths.
- Builds searchable static HTML package and build reports.
- Prints known-good QEMU boot and maintenance commands.

## Current Tuxenix Snapshot

Against the current local package tree, the toolkit reports:

```text
packages: 419
built artifacts present: 418
unbuilt/no dist archive: 1
```

The systemd report currently finds:

```text
Direct systemd deps: 7
Transitive systemd deps: 13
```

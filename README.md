# Tuxenix

**LFS-based Linux distribution workbench by elgun-dev**

I am building Tuxenix from the ground up: package recipes, a working root filesystem, a custom package flow, QEMU boot testing, and a usable lightweight desktop stack. This repo tracks the public-facing story of that work.

## Role

**Tuxenix Developer**

Focused on turning Linux From Scratch and BLFS source builds into a repeatable distribution workflow with real packages, real VM testing, and practical desktop/server usability.

## Related Tooling

The six support projects live in the public toolkit repo:

**https://github.com/elgun-dev/tuxenix-toolkit**

That repo includes:

- package recipe linter
- dependency graph generator
- package explorer
- build dashboard
- LFS/Tuxenix boot lab notes
- Tuxenix VM launcher/helper

## What This Project Is

Tuxenix is an experimental Linux distribution built around source-based packaging and repeatable system construction. The current development setup uses an LFS/BLFS userspace, a custom package manager flow, and QEMU for fast boot and install testing.

The goal is not just to compile packages. The goal is to make the system boot, install software, recover from bad package states, serve packages over HTTP, and run a usable graphical session.

## Current Milestone

- Built and staged **309 original packages**.
- Added **tty-clock** as package 310 and verified install through the package repo.
- Booted Tuxenix in QEMU using a host kernel with a Tuxenix userspace.
- Brought up **IceWM** and Xorg with virtio GPU support.
- Set up an HTTP package repository and verified `txpk` can fetch packages over the network.
- Validated a safe package install set with `safe100-result count=100 failed=0`.
- Repaired kernel-module, locale, xterm/UTF-8, and X startup issues in the VM image.

## Package Work

Recent package batches include terminal tools, file management, fonts, shells, and desktop components:

- `fish` and `fisher`
- `vifm`
- `pcmanfm`
- `libfm`, `libfm-extra`, `menu-cache`, `lxmenu-data`
- `nerd-font-jetbrains-mono`
- `tty-clock`

I also added package-purpose documentation across the tested package set so each recipe explains why the package matters to Tuxenix users or to the OS stack.

## Notable Fixes

- Fixed GLib packaging so real GLib libraries and pkg-config files are installed correctly.
- Patched Fish build behavior for current CMake policy handling.
- Fixed `libfm-extra` and `libfm` include installation so package archives preserve the expected headers.
- Patched `menu-cache` for GCC 15 compatibility.
- Patched `pcmanfm` for stricter compiler and GTK/ATK issues.
- Fixed Xorg startup by matching guest kernel modules to the host kernel used by QEMU.
- Added a `startx` wrapper so QEMU GPU modules load automatically.
- Generated and installed a working UTF-8 locale so `uxterm`, IceWM, and terminal apps render correctly.

## System Pieces In Motion

- **Package recipes:** `package.yml`, `build.sh`, and source archives under `os/1-lts/<package>`.
- **Package manager:** `txpk` for install/fetch testing.
- **Build flow:** `tx-build` inside a build chroot.
- **Repository:** local package repo synced to an HTTP server.
- **VM:** QEMU image used for real boot, install, and GUI validation.
- **Desktop:** Xorg, IceWM, xterm/uxterm, fonts, and lightweight file-manager stack.

## Why This Matters

This is low-level distribution engineering: package metadata, build scripts, runtime dependencies, filesystem layout, boot behavior, X11, kernel modules, package repositories, and VM testing all have to line up. Tuxenix is where I am putting those pieces together and proving them under a running system.

## Status

Active development. The system boots, installs packages from an HTTP repo, runs a lightweight GUI, and has a growing package set with tested recipes.

Next targets are cleaner package ownership, broader desktop usability, more reproducible VM setup, and continued BLFS package expansion.

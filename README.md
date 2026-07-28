# Tuxenix

**An LFS/BLFS Linux distribution built from source, packaged with `txpk`, and
booted by dinit.**

[Website](https://tuxenix.org/) ·
[Download ISO](https://tuxenix.org/iso/tuxenix-dinit-desktop-latest.iso) ·
[Package catalog](https://tuxenix.org/packages.html) ·
[Installation guide](https://tuxenix.org/install.html)

I am building Tuxenix from the ground up: package recipes, a custom package
flow, a bootable installer, a public package repository, a lightweight desktop,
and a native dinit service graph. This repository tracks the public story and
major engineering milestones.

## Latest Milestone: Public Dinit Desktop Release

Tuxenix is now a publicly downloadable, real-hardware-tested Linux desktop:

- **473 compiled package archives** are available from the public HTTPS
  repository.
- A **2.6 GiB hybrid BIOS/UEFI ISO** boots a live IceWM desktop and launches
  the Calamares installer.
- Installed systems use **dinit as PID 1**, with systemd-compatible runtime
  libraries only where the hardware and desktop stack require them.
- The installer contains a seeded and integrity-checked `txpk` database.
- `txpk` uses the public `https://tuxenix.org` repository with a working CA
  certificate path.
- NetworkManager, Wi-Fi, DNS, SSH, ALSA audio, Xorg, IceWM, and Brave are
  integrated into the desktop profile.
- Wi-Fi profiles created in the live environment are securely preserved for
  the installed system.
- The graphical desktop remains opt-in: log in and type `startx` to launch
  IceWM.

## Download and Verify

```sh
curl -O https://tuxenix.org/iso/tuxenix-dinit-desktop-latest.iso
curl -O https://tuxenix.org/iso/tuxenix-dinit-desktop-latest.iso.sha256
sha256sum -c tuxenix-dinit-desktop-latest.iso.sha256
```

Current ISO SHA-256:

```text
f5e3a7953fcb2bbb267af66b5ad65f763938767559239fa15fae6ff23ff1b58c
```

The full package catalog and direct archive downloads are available at
[tuxenix.org/packages.html](https://tuxenix.org/packages.html).

## Proven End to End

The current release has been exercised across the full distribution path:

- built packages from LFS/BLFS-oriented source recipes;
- generated a complete installed root filesystem and live installer;
- created El Torito BIOS and UEFI boot structures;
- booted the ISO through GRUB and reached the live installer in QEMU;
- installed and tested Tuxenix on a Lenovo ThinkPad;
- connected to Wi-Fi and verified reconnection persistence;
- launched IceWM with `startx`;
- ran Brave with working YouTube video;
- enabled ALSA audio, persistent volume state, and multimedia volume control;
- started OpenSSH automatically as a dinit-managed service;
- served the ISO and all packages from the public HTTPS repository;
- verified all 476 entries in the release checksum manifest; and
- streamed the public 2.6 GiB ISO back over HTTP and matched it byte for byte.

## Architecture

| Layer | Tuxenix implementation |
| --- | --- |
| Userspace | Linux From Scratch and Beyond Linux From Scratch foundations |
| Package format | `.txpk.tar.bz2` archives with `package.yml` metadata |
| Package manager | `txpk` |
| Init system | dinit |
| Networking | NetworkManager, `wpa_supplicant`, persistent connection profiles |
| Desktop | Xorg, IceWM, xterm, libinput, Liberation fonts |
| Browser | Brave |
| Audio | ALSA utilities, dinit state restoration, persistent volume |
| Installer | Live IceWM session with Calamares |
| Boot media | Hybrid BIOS/UEFI ISO |
| Repository | Static HTTPS package indexes at `tuxenix.org` |

## Native Dinit Boot Graph

The installed image enables native dinit services for:

- filesystems;
- kernel modules;
- NetworkManager;
- OpenSSH;
- ALSA state restoration; and
- the Tuxenix firewall.

The SSH service prepares its service account, runtime directories, and host
keys before executing `sshd -D`, allowing it to start automatically on a clean
installation.

## Notable Engineering Fixes

- Seeded the package database during image creation and validated it before
  completing the ISO.
- Shipped a correct `/etc/txpk/pkg.yml` for the public repository.
- Added explicit CA-bundle handling to the bundled `txpk` runtime.
- Preserved NetworkManager Wi-Fi profiles with root ownership and `0600`
  permissions.
- Made plain `startx` launch `icewm-session` for normal desktop users.
- Added a login message explaining that IceWM is available through `startx`.
- Fixed UTF-8 locale generation so IceWM menus and terminal applications do
  not crash.
- Preserved Brave's required sandbox ownership and setuid mode.
- Added audio, video, render, and input group access for desktop users.
- Added ALSA utilities, volume defaults, state restoration, and dB-mapped
  volume behavior.
- Built the required laptop audio codecs into the Tuxenix kernel.
- Added resumable, atomic release uploads and a forced-refresh mode for
  same-sized checksum or HTML files.

## Source and Tooling

- **Public project overview:** this repository
- **Toolkit and ISO builder:**
  [elgun-dev/tuxenix-toolkit](https://github.com/elgun-dev/tuxenix-toolkit)
- **Installer source (GitLab; sign-in may be required):**
  [Tuxenix installer dinit branch](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/tree/tuxenix-dinit-forge)
- **Package recipes and dinit services (GitLab; sign-in may be required):**
  [Tuxenix package sources dinit branch](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/tree/tuxenix-dinit-forge)
- **Public package repository:**
  [tuxenix.org/1-lts](https://tuxenix.org/1-lts/)

The toolkit provides package linting, dependency graphs, build dashboards,
root-filesystem generation, ISO creation, public catalog generation, release
uploading, and QEMU boot helpers.

## Installation Notes

Write the ISO to a USB drive and boot it through the machine's BIOS/UEFI boot
menu. In Calamares manual partitioning:

- choose the desired Linux partition, format it, and mount it at `/`;
- choose the EFI System Partition and mount it at `/boot/efi`; and
- only format the EFI partition when it is dedicated to Tuxenix and its
  existing contents are no longer needed.

After installation, connect to Wi-Fi if necessary, log in as the normal user,
and run:

```sh
startx
```

## Status

Active development. Tuxenix now boots, installs graphically, runs on real
laptop hardware, reconnects to Wi-Fi, serves packages publicly over HTTPS,
runs a dinit-managed desktop/server service graph, launches Brave, and plays
video with working audio.

Next targets include broader hardware validation, smaller live-media memory
requirements, package signing, stronger package-transaction recovery, and
continued LFS/BLFS package expansion.

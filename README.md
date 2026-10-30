# Tuxenix

Tuxenix is an x86_64 Linux distribution built from Linux From Scratch and
Beyond Linux From Scratch. It uses **dinit** for startup, **XLibre and IceWM**
for the desktop, and **txpk** to install packages from its own repository.

The project brings the whole system together: source recipes, compiled
packages, boot services, a live image and a graphical installer. The installed
system starts at a text login. Run `startx` when you want the desktop.

[Download](https://tuxenix.org/iso/tuxenix-dinit-desktop-2026-10-22.iso) ·
[Get started](docs/getting-started.md) ·
[Packages](https://tuxenix.org/packages.html) ·
[Release status](docs/status.md) ·
[Website](https://tuxenix.org/)

## Try Tuxenix

The current image is **October 22, 2026**, approximately **1.22 GiB**.
Installation uses **UEFI with Secure Boot disabled, a GPT disk and an ext4
root partition**. Allow at least 20 GiB for root. A VM with a blank virtual
disk is a useful place to start.

Download the dated image and its checksum into the same directory:

```sh
curl -fLO https://tuxenix.org/iso/tuxenix-dinit-desktop-2026-10-22.iso
curl -fLO https://tuxenix.org/iso/tuxenix-dinit-desktop-2026-10-22.iso.sha256
sha256sum -c tuxenix-dinit-desktop-2026-10-22.iso.sha256
```

Continue when verification reports `OK`. Follow the
[installation walkthrough](docs/getting-started.md) for booting, partitioning
and first login. Formatting the selected root partition erases its contents.

The October 22 image passed a complete automatic installation and boot from
the installed disk in QEMU. Physical hardware and real Wi-Fi association have
not been qualified for this image. Earlier laptop results and October 17
tests are recorded separately in the [test record](docs/status.md).

## What is in the system

| Part | Implementation | What it means in use |
| --- | --- | --- |
| Base | LFS/BLFS packages, x86_64 | Tuxenix maintains its own recipes and compiled archives. |
| Startup | dinit and native service definitions | Boot and service management do not require systemd as PID 1. |
| Desktop | XLibre, IceWM, `startx` | A window manager and desktop tools, launched from your normal account. |
| Packages | txpk, `.txpk.tar.bz2` archives | Install from the public `1-lts` HTTPS repository. |
| Networking | NetworkManager and `wpa_supplicant` | Configure connections in the installer or with `nmtui`. |
| Sound | ALSA and Sound Setup | Choose a playback device, test it and save its mixer state. |
| Installer | Calamares with Tuxenix modules and settings | Network setup, timezone selection and an explicit partition plan. |
| Graphics runtime | Native and i686 libraries | 32-bit applications have a separate runtime under `/usr/lib32`. |

The display server is XLibre; its package is still named `xorg-server` for
dependency compatibility. Some desktop applications use libraries supplied
by `systemd-compat`. That package does not make systemd the init system.

[How the system fits together →](docs/architecture.md)

## The work behind the image

Most of the distribution work happens where components meet:

- **An installation that boots on its own.** The installer prepares the
  target filesystem, package records and EFI files. Release tests remove the
  ISO before booting the installed disk.
- **A package database that describes real files.** Image construction
  checks package records against retained payloads. Setup tools can repair
  missing files when an older image still claims their package is installed.
- **A usable desktop under dinit.** NetworkManager, its Wi-Fi supplicant,
  device discovery and saved audio state need working service dependencies.
  Installing their binaries alone is not enough.
- **Tests that actually fail when the code fails.** Recent XLibre work fixed
  a test runner that hid child-process failures, then exposed and repaired an
  input-protocol bug. That patch is still pending release.

[Engineering notes: problems, changes and evidence →](docs/engineering.md)

## Released and in progress

Status recorded **October 29, 2026**:

| Work | State |
| --- | --- |
| October 22 installer ISO | Published; remains the current image. |
| `power-utils` 1.0.0 | Published October 29; adds `shutdown` and `reboot` using dinit. |
| New desktop controls, installer changes and XLibre fixes | Tested source changes in open merge requests; not a new ISO release. |

The next release needs a full installation test of the combined image.
Physical graphics acceleration, games, Wi-Fi and the new graphical power
controls also need their own results. Passing a VM test does not settle those
questions.

[Release details, test coverage and remaining work →](docs/status.md)

## About this repository

This is the public documentation and issue tracker for Tuxenix. It contains
installation notes, engineering records and a pinned package manifest for
the published image. The distribution's build sources live separately on
GitLab; access may require sign-in. See the [source map](docs/architecture.md#source-map)
for the active branches and their role.

To report a failure, include the image date, hardware or VM configuration,
steps to reproduce and the actual output. Reports of working hardware are
useful too, as long as they say what was tested.

[Report a bug](https://github.com/elgun-dev/Tuxenix/issues/new?template=bug-report.yml) ·
[Report hardware results](https://github.com/elgun-dev/Tuxenix/issues/new?template=hardware-report.yml) ·
[Contribute](CONTRIBUTING.md)

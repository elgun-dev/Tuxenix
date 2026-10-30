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
[Progress](docs/progress.md) ·
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

## Development progress

The recorded work runs from the first package builds in June to the current
installer and desktop integration. These milestones include experiments and
fixes as well as releases; the dates do not all represent downloadable images.

| Date, 2026 | Progress | Result at that stage |
| --- | --- | --- |
| June 9–13 | Established the project, staged 310 packages, booted the LFS/BLFS userspace in QEMU and brought up IceWM/Xorg. | HTTP package installs worked; a selected 100-package install check passed. |
| June 13–14 | Added recipe linting, dependency graphs, package/build reports and VM helpers; expanded firmware, networking and firewall packages. | A repeatable development workflow and a network stack ready for hardware testing. |
| July 28 | Published the dinit desktop with Calamares, txpk and an HTTPS package repository. | ThinkPad testing covered Wi-Fi, IceWM, Brave/video, audio and SSH. |
| August 5 | Published a smaller, roughly 935 MiB image; repaired runtime dependencies and boot setup. | Image structure and USB readback verified; full graphical/physical installation still needed testing then. |
| September 17 | Added manual partition creation/editing, queued changes, Revert and layout validation alongside empty-drive setup. | A blank-disk VM installation booted independently. |
| September 21 | Added shared-ESP installation and reinstallation that preserve existing loaders and partitions. | VM checks preserved neighboring data and booted both entries. |
| September 28 | Fixed package ownership/mode ordering that stripped setuid/setgid permissions. | Installed-system `sudo`, `su`, password changes and normal-user desktop passed. |
| October 1 | Integrated XLibre and its matching input driver. | Experimental install, desktop/input and virtual graphics tests passed; a test-runner defect remained. |
| October 8 | Fixed legacy EFI-directory handling and unclear root-format/readiness controls. | Reinstallation preserved neighboring data; the new system booted without the ISO. |
| October 12 | Fixed firmware-entry lookup and published the corrected ISO and redesigned website. | VM installation and public-download checks passed; physical laptop installation was user-confirmed. |
| October 15 | Published 31 multilib/runtime packages, including the 32-bit library stack and Steam support. | Native and i686 libraries stayed separate; Steam startup was user-confirmed on the laptop. |
| October 16 | Published Intel graphics/setup improvements, desktop repair/timezones, and AMD/open NVIDIA graphics and sound tools. | VM update, repair and startup checks passed; physical GPU/game coverage remained open. |
| October 17 | Published a new image combining graphics, desktop tools, firmware and installer fixes. | Clean/shared-ESP installs, disk-only boot, normal-user desktop and Steam sign-in passed in VMs. |
| October 19–22 | Added installer networking, partition units, GPT-only creation, automatic EFI flags and readable dialogs. | October 22 ISO published after final automatic-install and disk-only boot checks. |
| October 26 | Added graphical Wi-Fi/power controls, an installer redesign and a Try/Install chooser. | Source and preview work; not a published replacement ISO. |
| October 29 | Published `power-utils`; completed XLibre/multilib/dinit integration and repaired the hidden test failures and protocol bug. | Power commands released; integration tests passed and source merge requests remain open. |

[Read the full progress log: changes, setbacks, tests and release boundaries →](docs/progress.md)

## Current release and next work

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

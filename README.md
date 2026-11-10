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
| October 29 | Published `power-utils`; completed XLibre/multilib/dinit integration and repaired the hidden test failures and protocol bug. | Power commands released; integration tests passed and merge requests opened. |
| October 30 | Added Easy/Expert installer modes and rebuilt the image with current desktop utilities and XLibre fixes; pushed source for merge. | Fresh installation, disk-only boot, normal-user desktop and graphical shutdown passed. Candidate ISO remains unpublished. |
| November 5 | Added Easy-mode installation in existing unallocated space, explicit EFI selection and preserving boot setup. | Linux VM installation, refusal guards and 4Kn/multiple-ESP checks passed; Windows testing remained open. |
| November 9 | Tested genuine Windows and protected BitLocker, fixed Windows EFI checks, first-install boot entries on other ESPs and udev readiness. | Combined settings 1.5.13/services 0.1.14 image passed the final VM matrix; website status is published, while protected source merges and binary deployment remain pending. |

[Read the full progress log: changes, setbacks, tests and release boundaries →](docs/progress.md)

## Current release and next work

Status recorded **November 9, 2026**:

| Work | State |
| --- | --- |
| Public download | October 22 remains published; the qualified November 9 replacement awaits protected source merges and verified binary deployment. |
| Website | [Current status and test results](https://tuxenix.org/status.html) are published and HTTPS-verified; ISO and package downloads are unchanged. |
| Easy-mode alongside installation | Implemented for existing unallocated GPT space; existing partitions are kept and the selected EFI partition is reused without formatting. Automatic shrinking is not implemented. |
| Windows and BitLocker | Genuine Windows install/reinstall, partition and EFI preservation, both desktops, BitLocker recovery/reseal and protected subsequent boot passed on the exact combined replacement. |
| Current replacement | Calamares 3.4.2.23, settings 1.5.13, dinit services 0.1.14 and 289 pinned archives. See the exact artifact and test matrix in the status record. |
| Source and release | Existing [package MR !5](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/merge_requests/5) and [installer MR !3](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/merge_requests/3); protected merges and verified publication remain required. |

The current work closes the gap between a prepared partition plan and a
reliably bootable dual-boot system. Tests compare entire existing partitions
and EFI files before either old operating system starts, then check both
boot choices. The latest fixes also make first installation onto a different
ESP retain the old Tuxenix menu entry and wait for udev before device events.

Next: complete administrator-approved protected source merges, refresh the
release staging from the current website, publish the ISO and packages, and
verify the public files over HTTPS. Qualification and website review are complete.
Physical graphics, real Wi-Fi, games, suspend, hardware TPM and Secure Boot
still need separate
results. The working laptop is not a disposable test target.

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

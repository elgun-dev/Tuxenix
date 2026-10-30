# Tuxenix development progress

[← Tuxenix](../README.md) · [Current release and tests](status.md) · [Engineering notes](engineering.md)

This is the recorded progression from June 9 through October 29, 2026.
Dates identify when a milestone was recorded or released. A development ISO,
a successful VM test and a published image are different milestones; each
entry keeps that distinction. Historical commands and old installer behavior
are described here, not recommended as current installation instructions.

## June 9–13 — package collection to a running system

The public repository began on June 9. By June 13, the project record listed
309 staged packages, with `tty-clock` added as number 310. The development
system booted an LFS/BLFS userspace in QEMU using a host kernel and reached
IceWM on Xorg with virtio graphics.

An HTTP repository served packages to `txpk`. A selected 100-package install
check reported 100 successes and no failures. This established a working
package-install path, not validation of every package in the collection.

Work included Fish, Vifm, PCManFM, its supporting libraries and fonts. Fixes
addressed missing GLib payloads, header installation, newer compiler/CMake
behavior, matching kernel modules and usable UTF-8 locales. These were the
practical problems between a successful build and a working application.

[June 13 project record](https://github.com/elgun-dev/Tuxenix/blob/61d1123/README.md)

## June 13–14 — tooling and networking

The support toolkit grew to include recipe linting, dependency graphs,
package exploration, build reports and QEMU launch helpers. It gave the
package collection a way to expose missing inputs and dependencies.

Networking work added firmware, Wi-Fi authentication, DHCP/DNS components,
NetworkManager, regulatory data, diagnostics and inbound firewall defaults.
Build-chroot DNS and CA-certificate setup also needed attention so a recreated
build environment could fetch sources over HTTPS.

The package set targeted common PC/laptop hardware; that was a development
target, not proof that every adapter worked. Broader hardware validation
remained a next step.

[June 14 networking record](https://github.com/elgun-dev/Tuxenix/blob/7a00c53/README.md)

## July 28 — public dinit desktop

The project reached a public desktop image with dinit as PID 1, IceWM,
Calamares and a seeded txpk database. The public repository held 450 package
names and 473 compiled archives at this point. The image was approximately
2.6 GiB.

Native dinit services brought up filesystems, device discovery, networking,
SSH, audio-state restoration and the firewall. The compatibility libraries
needed by applications stayed separate from the choice of init system.

ThinkPad testing covered Wi-Fi and reconnection, `startx`, Brave with YouTube
video, ALSA audio, saved volume state and automatic SSH. The public image and
release files were checked by downloading them and comparing hashes.

This was meaningful physical-hardware progress. Those results belong to that
installation and should not silently become qualification of every later ISO.

[July public release record](https://github.com/elgun-dev/Tuxenix/blob/33c14c6/README.md)

## August 5 — smaller image and boot repairs

The published fixed6 image reduced the download to 980,332,544 bytes, about
935 MiB. It had 205 target packages and 241 live packages. It still exceeded
the then-preferred 640 MiB target.

The work corrected `iproute2`'s missing `libmnl` runtime dependency, made
loopback setup recoverable, created the machine ID without systemd tools and
kept dinit/IceWM as the installed defaults. The installer used Limine and
identified the installed root by PARTUUID.

Static image, runtime-library, package-database and boot-configuration checks
passed. QEMU reached the dinit handoff and a full USB readback matched the
image hash. Complete graphical boot and physical installation were still
unverified in that release record.

The installer at this stage replaced files on the selected EFI partition.
The preserving shared-ESP workflow came later; August behavior is not the
current installation procedure.

## September 17 — usable manual partitioning

Calamares 3.4.2.5 and configuration 1.4.7 added manual controls alongside
automatic empty-drive setup: create a GPT table, create/edit/delete partitions,
change supported sizes and revert the proposed layout. Invalid root/EFI
assignments kept Next disabled. Edits remained queued until Install.

A disposable UEFI VM exercised a blank 32 GiB disk, changed a proposed root
from 20 to 24 GiB, checked deletion and Revert, and measured zero target writes
through Summary. A manual install with a 512 MiB FAT32 ESP and ext4 root then
booted to login with the ISO removed.

The user trial exposed another problem: important partition controls sat
below the visible area of a small installer window. That made the workflow
hard to discover despite passing its functional tests. Later layout work
addressed the visibility and sizing of these controls.

This was development-image work. Shared-ESP preservation was not yet present.

## September 21 — preserve other installations

Calamares 3.4.2.6 and configuration 1.5.1 added installation into unallocated
space while reusing an existing FAT32 EFI System Partition without formatting
it. Tuxenix wrote its own EFI files, retained foreign loaders and firmware
entries, checked free space and reused its entry on reinstall.

A VM with a shared ESP and an existing Linux fixture completed installation
and reinstallation. Raw checksums showed the neighboring root and preexisting
EFI files were unchanged. Both boot entries worked, the installed Tuxenix
booted without its ISO, and reinstallation retained one Tuxenix firmware entry.

The fixture was not Windows. These results established preservation behavior
under the tested layout, not general Windows/BitLocker or Secure Boot support.

## September 28 — ownership and permissions

Package copying and installation restored permissions before changing file
ownership. On files with setuid/setgid bits, the later ownership change cleared
those bits. An archive could appear to install correctly while leaving
administrative commands unusable.

The builder and package manager were changed to restore modes after ownership.
Shadow and sudo were rebuilt with the corrected tooling. Regression tests
covered the ordering, and the installed VM authenticated `su` and `sudo`,
changed a password with `passwd`, logged in with the new password and reached
a normal-user IceWM session.

This repaired a system-integration failure that package presence alone could
not detect. Older archives with stripped bits still needed rebuilding.

## October 1 — XLibre experiment

The display server moved to XLibre 25.1.9, paired with input driver 25.0.1.
The package remained `xorg-server` and retained `Xorg`/`X` command names so
existing dependencies and launchers continued to work.

The experimental image installed in a UEFI VM, booted independently and ran
IceWM as an ordinary user. Input, resolution changes, software rendering and
a separate virtual VirGL graphics path were exercised. Virtual acceleration
did not establish physical GPU support.

A server assertion also exposed an unreliable test harness: a failed child
could leave a successful exit code and prevent later cases from running.
That remained a recorded issue until the October 29 work. XLibre itself
reached the public image on October 12; the later patched candidate is a
separate change.

## October 8 — legacy EFI folders and clearer readiness errors

An installation encountered an existing `EFI/Tuxenix` directory without the
new ownership marker. The helper was changed to preserve that directory and
use a root-specific path when ownership could not be established. Reinstalling
the same root reused its path and firmware entry.

A second problem was an apparently unexplained disabled Next button after
assigning `/` and `/boot/efi`. The old UI could leave root set to Keep even
though installation required formatting. The new flow explicitly asked for
root-format confirmation, kept an existing ESP unformatted and explained
individual readiness failures.

VM reinstallations preserved neighboring partitions and old EFI files, then
booted the new root without the ISO. These were fixes under development; the
physical installation path still needed another round of testing.

## October 12 — firmware lookup fixed and installation confirmed

The next physical failure was traced to `efibootmgr --bootnum ... --active`.
Upstream efibootmgr 18 could miss a matching firmware entry when other entries
followed it. A VM reproduced the same ordering and exit failure.

Package 18.1 applied the lookup fix. The installer helper avoided redundant
firmware writes, verified the active entry and BootOrder, and retained command
stderr in its failure dialog. The regression failed before the patch and
passed afterward.

The finished 997,081,088-byte image passed UEFI/NVMe installation, disk-only
boot, preservation checks and normal-user sudo/IceWM. After the corrected USB
was tested on the laptop, the user confirmed that installation worked. The
ISO was published and its complete HTTPS download matched the recorded hash.

The website was also redesigned around a compact download page, installation
guide and package catalog. Responsive layout and navigation were checked.

[October 12 published release](https://tuxenix.org/releases.html#2026-10-12-installer)

## October 15 — multilib and Steam

Thirty-one runtime/diagnostic packages were published: 27 `lib32-*` packages,
the multilib kernel, runtime and test packages, and the Steam package. The
repository reached 481 names and 507 archives.

The i686 libraries lived under `/usr/lib32` while native libraries stayed in
`/usr/lib`. Steam's downloaded user runtime remained separate again. Package
and runtime checks had to prove that adding 32-bit support did not replace
the native system libraries.

Steam startup on the user's laptop was confirmed. The setup process had still
been difficult: dependency downloads, kernel activation, readiness checks and
failure reporting needed to be clearer. That experience informed the setup
helpers and explicit update flow added next. Client startup alone was not a
game or Proton compatibility result.

## October 16 — graphics, desktop repair and repeatable setup

Three published update groups addressed different parts of everyday setup:

- **Intel graphics and Steam setup:** firmware, i915/Xe kernel modules,
  32-bit HASVK support, readiness checks, explicit component updates and
  separate guarded kernel activation. Txpk gained clearer CLI operations,
  progress and diagnostic logging.
- **Desktop repair and timezones:** explicit reinstallation restored missing
  Python files despite stale package records. ALSA tools, timezone data,
  timezone selection and battery percentage defaults were added or repaired.
- **Graphics and sound tools:** AMD firmware and open NVIDIA Nouveau/NVK
  support, 32-bit Mesa drivers, Graphics Setup and Sound Setup. Short command
  names such as `desktop-setup`, `battery-status` and `timezone-config` retained
  compatibility aliases.

VM tests covered updates, reboot, repeat setup, missing-file repair and Steam
sign-in. The graphics checker correctly rejected software rendering as proof
of hardware readiness. On the existing laptop, the user separately confirmed
sound after the muted mixer was corrected; reboot persistence was not yet
confirmed in that report.

These package releases did not rewrite the October 12 ISO. Physical AMD/NVIDIA
acceleration, game performance and hybrid GPU behavior still required testing.

[Intel/setup release](https://tuxenix.org/releases.html#2026-10-16-intel) ·
[Desktop repair release](https://tuxenix.org/releases.html#2026-10-16-desktop) ·
[Graphics and sound release](https://tuxenix.org/releases.html#graphics-2026-10-16)

## October 17 — the combined graphics desktop image

A new 1,313,755,136-byte image brought together the multilib kernel, XLibre,
GPU/network firmware, native/i686 libraries, desktop setup tools, Python,
ALSA and timezone data. Twelve package updates accompanied it. Steam remained
an optional download.

Tests covered shared-ESP installation and manual installation on a blank disk,
booting without the ISO, normal-user desktop/sudo, timezone persistence,
repeat setup and Steam sign-in. Neighboring partitions and foreign EFI files
remained unchanged. Selected 2 GiB live-boot configurations also worked.

BIOS with standard VGA failed graphical startup. BIOS/virtio live boot was a
separate result; installation remained UEFI-only. Physical GPU/game and broader
laptop behavior were not established by these VM results.

[October 17 published release](https://tuxenix.org/releases.html#installer-2026-10-17)

## October 19–22 — installer networking and partition usability

GPT-only table creation began as a source change on October 19. The October 22
release combined it with a Network page, saved connection transfer, selectable
partition units, automatic EFI flags and more readable dialogs/display sizing.

Unit-only changes preserved partition geometry. Network fixtures covered SSID
escaping, BSSID selection, password transport and offline continuation. The
final ISO completed automatic installation to a blank 64 GiB QEMU disk and
booted independently. Target writes stayed at zero through Summary; a synthetic
Wi-Fi profile retained its contents and restrictive ownership/permissions.

The published image is 1,313,968,128 bytes. Its installed-system payload remains
the October 17 base. Physical Wi-Fi association was not tested for this image.
This is still the latest published ISO as of October 29.

[October 22 published release](https://tuxenix.org/releases.html#installer-2026-10-22)

## October 26 — desktop controls and installer redesign

Source changes added a graphical Wi-Fi adapter/network picker, connection
controls and authentication for changes. Power controls offered confirmed
Shutdown, Restart and Log Out. Lock and Suspend were not implemented.

The installer gained a website-aligned blue palette, smaller controls, a custom
window header, a redesigned welcome page and a Try/Install chooser. Try kept
the live desktop running. The preview's installed payload was still October 22.

Builds, targeted tests and preview navigation passed, including reporting that
no wireless adapter was present in the VM. Actual wireless association,
complete installation of the new package set and successful graphical power
and authentication flows were not all qualified. The changes were saved and
pushed as source; the preview was not a new public ISO.

## October 29 — power release and tested source integration

`power-utils` 1.0.0 was published as a small, separate package for `shutdown`
and `reboot`. Moving the wrappers out of a proposed dinit update avoided
replacing PID 1 and pulling a compiler for a two-command change. The released
archive passed real VM reboot and poweroff checks while preserving the core
runtime hashes. The ISO remained October 22.

The newer Tuxenix source branches were synchronized with their repositories'
main branches, and release integration was collected in package MR !4 and
installer MR !3. The installer fix includes power-utils in installed dinit
profiles. Both merge requests remained open; this did not merge them into main.

The XLibre work finally repaired child-failure propagation in the test runner.
Previously hidden cases exposed stale fixtures and a real passive-grab bug:
byte-array event masks were being swapped along with integer modifier words
for opposite-byte-order clients. The patch swaps only the modifier words.

Eight available server tests, both input tests, 105 package Python tests and
six harness scenarios passed; external XTS/Piglit remained skipped. Final
candidate archives were installed in a fresh guest and checked against their
payload hashes. Normal-user desktop/input, resolution changes, software OpenGL,
reboot and shutdown passed; core runtime and all 444 checked lib32 file hashes
were unchanged.

The server candidate is 25.1.9.1. It and the new desktop/installer work remain
unpublished integration work. A full new-image installation, physical hardware,
games and graphical power/authentication still need their own qualification.

[Power command release](https://tuxenix.org/releases.html#power-2026-10-29) ·
[Exact integration revisions and remaining work](status.md#pending-source-integration)

## Evidence and maintenance

The early milestones come from the dated GitHub snapshots linked above.
August–October development history is recorded in the package source tree's
[dated project record](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/blob/c4d9d1247fdd5d0a42ccae8a2d8ae0339996159b/ai-context.md),
with focused [XLibre notes](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/blob/c4d9d1247fdd5d0a42ccae8a2d8ae0339996159b/docs/xlibre.md)
and [multilib notes](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/blob/c4d9d1247fdd5d0a42ccae8a2d8ae0339996159b/docs/multilib.md).
The installer repository records the
[October 26 source work](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/blob/0ebcb59db57bc21bb60ebf57f562ea98b3533304/docs/progress-2026-10-26.md).
GitLab may require sign-in. Published milestones are also linked to the public
release timeline throughout this page.

Add future entries with the date, the problem addressed, what changed, what
was actually tested and whether an artifact was published. Preserve the
original scope of historical tests when newer images supersede them.

# Engineering notes

[← Tuxenix](../README.md) · [Architecture](architecture.md) · [Test record](status.md)

These are concrete problems encountered while turning the package collection
into an installed desktop. The dates distinguish released fixes from source
work still awaiting an image release.

## Package records must match the image

An older image retained an installed-package record for Python while omitting
files needed by desktop tools. Asking the package manager to install an
already recorded package could skip it, leaving the original failure intact.

The repair had two parts: retain Python, ALSA tools and timezone data in new
images, and make setup check the actual files. The published `txpk` 0.0.7
supports explicit reinstallation for this repair path. Desktop setup uses
that path when records and files disagree.

The October 17 work tested installation, repair and a second setup run in a
disposable VM, checking that core libraries, Bash and the display server were
preserved. The October 22 image retains that system payload. Its pinned
[package manifest](releases/2026-10-22-packages.json) records the inputs for
both live and installed roots.

This distinction also matters during builds: a cached archive can have the
expected filename while being older than its current recipe. Source revision,
package version and archive hash all belong in the release record.

## A partition plan must stay a plan until Install

The installer has to support an empty disk and a disk with existing data.
Those operations need different defaults. Whole-drive setup proposes a fresh
EFI partition and root. Manual setup can reuse an existing ESP without
formatting it, while requiring an explicit root-format decision.

October 22 added GPT-only table creation, automatic EFI flags and partition
size units. Unit conversion must not silently change a partition's geometry:
regression cases cover six units and both 512-byte and 4096-byte sectors.

The final image was tested against a blank 64 GiB QEMU disk. Write counters
stayed at zero through Summary; installation then produced the expected GPT,
512 MiB FAT32 ESP and ext4 root. The ISO was detached before testing boot.
Earlier October 17 shared-ESP tests checked neighboring partitions and foreign
EFI files. Those are separate results, not a claim of Windows/BitLocker support.

## Network setup must survive the live session

A connection established in the installer is only useful after reboot if its
profile reaches the installed system with the right permissions. The
October 22 test copied a synthetic NetworkManager Wi-Fi profile byte-for-byte,
with root ownership, mode `0600`, and a containing directory at `0700`.

Network fixtures also exercised escaped SSIDs, BSSID selection, offline
continuation and password transport over standard input instead of process
arguments. The guest's Ethernet connection worked. A synthetic profile and
virtual Ethernet do not test association with a physical wireless adapter;
that remains an explicit gap for this image.

## Power commands should not require replacing init

An early candidate put `shutdown` and `reboot` wrappers in a new dinit
package. Testing showed that this made a small command update carry an init
upgrade and a compiler dependency download.

The published October 29 fix puts the wrappers in `power-utils` 1.0.0, a
488-byte archive. Dinit stays at 0.20.0. On an installed system, txpk may fetch
dinit's archive for dependency metadata, but only `power-utils` is installed.

The exact released archive was installed in a fresh overlay of the October 22
VM. Reboot produced a guest-requested reset and a new boot ID. Shutdown
produced a guest-requested poweroff. Dinit, its backend, Bash and libc hashes
stayed unchanged. The commands use dinit's argument syntax; they do not
implement systemd-style shutdown scheduling.

## A green test summary hid a real XLibre bug

The XLibre unit runner could retain a successful exit code after a later child
process aborted. The summary looked successful even though assertions had
failed and later tests had not run.

The October 29 source work first fixed child-failure propagation. Running the
previously hidden cases exposed stale fixtures and a real protocol bug in
`ProcXIPassiveGrabDevice`: opposite-byte-order clients had their event-mask
bytes swapped along with modifier integers. The event mask is a byte array;
only the following modifier words should be swapped.

The patch preserves the mask and swaps the modifier words. Regression cases
check native and swapped clients, exact mask bytes, modifiers, reply counts
and invalid-mask errors. Separate harness checks ensure that success followed
by `SIGABRT` really fails.

All eight available server Meson tests and both input-driver tests passed.
The optional external XTS/Piglit suite was skipped. The final candidate pair
was installed in a disposable guest and tested with normal-user desktop,
keyboard/mouse input, resolution changes, software OpenGL, reboot and shutdown.

**This is tested source awaiting the protected GitLab main merge.** The candidate server is package
25.1.9.1; the published image contains 25.1.9. See the
[package merge request](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/merge_requests/4)
and [exact tested revisions](status.md#source-integration).

## What a release claim needs

A package build, a passing test suite, an installed guest and a public download
answer different questions. Release records keep them separate:

1. Pin the source revision and archive hashes.
2. Check the package payload and its runtime dependencies.
3. Install into a disposable system and exercise the changed behavior.
4. For an ISO, test the finished image through installation and disk-only boot.
5. After publication, read the files back over HTTPS and compare hashes.

These steps make failures easier to locate. They also keep a successful
software-rendered VM session from becoming an unsupported claim about laptop
graphics, Wi-Fi, sound or games.

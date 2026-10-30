# Release and test status

[← Tuxenix](../README.md) · [Get started](getting-started.md) · [Full progress log](progress.md)

Recorded **October 30, 2026**. Image releases, package updates and source
integration are listed separately because they reach users at different times.

## Published image: October 22

| Field | Value |
| --- | --- |
| Download | [tuxenix-dinit-desktop-2026-10-22.iso](https://tuxenix.org/iso/tuxenix-dinit-desktop-2026-10-22.iso) |
| Size | 1,313,968,128 bytes; approximately 1.22 GiB |
| Architecture and installation | x86_64; UEFI, GPT, ext4; Secure Boot disabled |
| Installed-system base | October 17 |
| Installer | Calamares 3.4.2.16; calamares-settings-tuxenix 1.5.8 |
| Kernel | Package 7.0.11.3; runtime `7.0.11-r3-tuxenix-multilib` |
| Init | dinit 0.20.0; tuxenix-dinit-services 0.1.13 |
| Display | XLibre server package 25.1.9; input driver 25.0.1 |
| Package inputs | [288 pinned archives](releases/2026-10-22-packages.json), with hashes and destination roots |

SHA-256:

```text
8ae76d8d70ffc346c675ba66cbea269b6d2bb9f470c9f94b43e0a5cd9286fc9e
```

The installer update adds network setup, saved connection transfer, partition
size units, GPT-only table creation, automatic EFI flags and improved dialog
sizing. It retains the October 17 installed-system payload.

The release record reports full HTTPS hash verification of all 21 publication
files. See the [published notes](https://tuxenix.org/releases.html#installer-2026-10-22)
and [source validation record](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/blob/a3399119c6b72e51c2a6aeb35529521e931f1339/docs/releases/2026-10-22-validation.md).
GitLab links may require sign-in.

## October 22 test coverage

| Area | Result and scope |
| --- | --- |
| Automatic installation | Final October 22 ISO installed to an empty 64 GiB QEMU disk; GPT, 512 MiB FAT32 ESP and ext4 root. |
| Writes before confirmation | Zero target writes through Summary in the final-image test. |
| Independent boot | Installed system reached login after the ISO was detached. |
| Networking | Virtual Ethernet worked; a synthetic Wi-Fi profile survived transfer with root ownership and restrictive permissions. |
| Installer regression checks | Four compiled suites, 41 toolkit tests, configuration checks and the runtime-library audit passed. |
| Manual empty-disk installation | Earlier October 22 candidate passed with a 20.5 GiB root; this was not the final-image automatic test. |
| Shared ESP and neighboring data | October 17 base tests preserved foreign EFI files and neighboring partitions. Not repeated in full for October 22. |
| Desktop, sudo, timezone and Steam sign-in | Passed in October 17 VM tests; not all repeated for the October 22 installer update. |
| Earlier laptop use | User-confirmed Steam startup and audio belong to an earlier installation, not qualification of the October 22 image. |

Real Wi-Fi association, physical graphics acceleration, games/Proton, hybrid
GPU behavior, battery/suspend and physical audio remain outside the final
October 22 qualification. Secure Boot and Windows/BitLocker are unvalidated.
Installation is UEFI-only; earlier BIOS live-boot tests do not imply BIOS
installation support.

## Published package: power-utils 1.0.0

Released **October 29**. This supplies `shutdown` and `reboot` wrappers for
the existing dinit backend. It does not replace the ISO or upgrade PID 1.

Install with `sudo txpk --install power-utils`. After saving work,
`sudo shutdown` powers off immediately and `sudo reboot` restarts. Options
follow dinit syntax; `shutdown now` is not a supported scheduling form.

The exact 488-byte archive passed txpk installation, command ownership and
path checks, actual guest-requested reboot, a changed boot ID, and actual
poweroff in a disposable October 22 VM overlay. Dinit, its shutdown backend,
Bash and libc hashes stayed unchanged. All 10 publication files passed full
HTTPS hash verification.

The repository discovery check at publication counted **495 package names and
549 archives**. Archives include retained versions, so this is not a count of
549 distinct packages. The website and catalog can change after this snapshot.

[Published package notes](https://tuxenix.org/releases.html#power-2026-10-29) ·
[Exact archive and hash](releases/2026-10-29-status.json)

## Source integration

The tested package and installer work is committed and pushed to GitLab review
branches. Direct pushes to protected `main` were rejected; the requested GitLab
merge remains pending. The private GitHub toolkit main has the tested installer
source. Complete the GitLab merges through [package MR !4](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/merge_requests/4)
and [installer MR !3](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/merge_requests/3).

| Repository | Pushed review revision | Candidate runtime revision |
| --- | --- | --- |
| Packages | [`e29a76b`](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/commit/e29a76ba7804bc2d8a5b896ad1764a070c40492a) | `3d7890d` |
| Installer | [`2eb1e22`](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/commit/2eb1e22baa7317b0178da3fe2dec639ca9303cc8) | `0ebcb59` |

Local merge and documentation commits preserve the tested runtime code.
The XLibre fix repairs both hidden child-process test failures and a real
input-protocol bug. Eight available server tests, both input tests and 105
package Python tests passed; external XTS/Piglit was skipped.

## October 30 candidate: Easy and Expert installer

This is a tested local image, **not a published download**. Easy mode is the
default: select an empty drive and prepare GPT, a 512 MiB FAT32 EFI System
Partition, and the remaining usable space as ext4 root. An occupied drive is
rejected. Expert retains the existing full partition controls. The title-bar
button switches modes; a manual plan must be explicitly reverted before
returning to Easy. No disk writes occur until installation is confirmed.

| Field | Value |
| --- | --- |
| File | `tuxenix-desktop-2026-10-30-candidate.iso` |
| Size | 1,340,993,536 bytes |
| Installer | Calamares 3.4.2.21; settings 1.5.9 |
| Desktop utilities | desktop-utils 1.0.6; xinit 1.4.4.6; power-utils 1.0.0 |
| Display | XLibre server package 25.1.9.1; input driver 25.0.1 |
| Inputs | [289 pinned archives](releases/2026-10-30-packages.json); 262 target packages, 285 live packages |

SHA-256:

```text
20a1de35dc8cbbeae95bd4ceef840cd7d9624b9116df094c0c321a2ec1105ec7
```

| Check | Result |
| --- | --- |
| Source tests | 41 toolkit tests and six compiled installer suites passed, including synchronous model-reset regression coverage. |
| Runtime libraries | Live and installed payload audits passed; no missing dependencies in 2,253 live and 2,004 target ELF files, including 363 32-bit files in each root. |
| Mode controls | Repeated resets, plan preservation, explicit Revert and occupied-drive rejection passed. |
| Final-image installation | Fresh Easy installation passed; zero target writes through Summary. |
| Independent boot | Installed disk booted through Limine and dinit with the ISO removed. |
| Desktop and versions | Normal-user desktop and installed package versions verified. |
| Wi-Fi window | Opened and reported wired networking/no wireless adapter in the VM; no real Wi-Fi association tested. |
| Graphical shutdown | Normal-user password authentication succeeded and the guest actually powered off. |

## Remaining qualification and publication

Physical graphics acceleration, games/Proton, real Wi-Fi association, suspend,
Secure Boot and Windows/BitLocker remain unqualified. Graphical restart was not
separately repeated on this final image. Earlier shared-ESP tests remain dated
historical evidence, not a repeat on this candidate. The working laptop was
not upgraded or reinstalled.

Publishing the candidate binaries and updating the public download are separate
release steps. The [handoff](handoff-2026-10-30.md) records what to continue from.
Report hardware results with the
[hardware form](https://github.com/elgun-dev/Tuxenix/issues/new?template=hardware-report.yml).

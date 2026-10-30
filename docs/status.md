# Release and test status

[← Tuxenix](../README.md) · [Get started](getting-started.md) · [Full progress log](progress.md)

Recorded **October 29, 2026**. Image releases, package updates and source
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

## What has been tested

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

## Pending source integration

The October 29 handoff records these merge requests as **open and mergeable**.
The source repositories' `main` branches had not received them:

- [Package MR !4](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/merge_requests/4):
  XLibre, multilib, dinit and desktop integration on `tuxenix-steam-multilib`.
- [Installer MR !3](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/merge_requests/3):
  installer and desktop integration on `tuxenix-steam-publication`, including
  `power-utils` in all installed dinit profiles.

| Repository | Tested runtime code | Documentation head at handoff |
| --- | --- | --- |
| Packages | `8c6380bee60cb47b0ed61d27f11ce989f506b6ce` | `c4d9d1247fdd5d0a42ccae8a2d8ae0339996159b` |
| Installer | `fed77f0068fae0b0486d08c4fbeacd1ed2193a5c` | `0ebcb59db57bc21bb60ebf57f562ea98b3533304` |

The XLibre candidate uses server package 25.1.9.1 and input 25.0.1. Eight
available server tests, both input-driver tests, 105 package Python tests and
six harness scenarios passed; external XTS/Piglit was skipped. A fresh guest
passed normal-user desktop, keyboard/mouse input, resolution change, software
OpenGL, sudo reboot and shutdown. Installed candidate payloads matched their
archives; core runtime and all 444 checked lib32 file hashes were preserved.

These results cover the tested source integration. The redesigned installer,
new graphical desktop controls and patched server are not a new published
ISO. The [XLibre engineering note](engineering.md#a-green-test-summary-hid-a-real-xlibre-bug)
explains the runtime fix and the previously misleading test results.

## Work needed before the next image release

| Work | Completion evidence needed |
| --- | --- |
| Combined image | Build from pinned inputs, install the finished ISO and boot without live media. |
| Graphical Wi-Fi and power controls | Complete connection and password-authenticated actions as a normal user. |
| Physical hardware | Dated results identifying the adapter/GPU, driver, firmware and actual behavior. |
| Graphics and games | Native and 32-bit acceleration checks, followed by named game/workload results. |

These are qualification gaps, not promised delivery dates. Report a result
with the [hardware form](https://github.com/elgun-dev/Tuxenix/issues/new?template=hardware-report.yml).
The public [release timeline](https://tuxenix.org/releases.html) records when
packages and images become available.

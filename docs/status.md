# Release and test status

[← Tuxenix](../README.md) · [Get started](getting-started.md) · [Progress](progress.md)

Recorded **November 9, 2026**. The current public download is still the
October 22 ISO. The combined November 9 replacement passed its complete VM qualification.
Protected source merges and verified deployment are still pending; it is not
yet a published download. The [website status update](https://tuxenix.org/status.html)
is live and HTTPS-verified. Its homepage, installation-guide note and release
notes changed without changing any ISO or package download.

This is the canonical current status and release handoff. Dated historical
records retain the evidence and limitations of their own images.

## November 9 replacement

Easy mode now supports installation into existing unallocated GPT space.
Choose the new root size and an existing EFI System Partition to keep.
Existing partitions are preserved; automatic shrinking is not implemented.
Expert retains manual controls and explicit root-format decisions. A plan
is revalidated immediately before installation, including checks for changed
disk layout and altered queued operations.

| Artifact | Value |
| --- | --- |
| Local candidate | `tuxenix-desktop-2026-11-09-candidate.iso` |
| Size | 1,329,913,856 bytes |
| Installer | Calamares 3.4.2.23; settings 1.5.13 |
| Boot services | dinit 0.20.0; tuxenix-dinit-services 0.1.14 |
| Display | XLibre server package 25.1.9.1; input driver 25.0.1 |
| Inputs | [289 pinned archives](releases/2026-11-09-packages.json); 262 target / 285 live packages |
| Package runtime source | `dbe763d47e0faad099dfca3113e7cefeffad728d` |
| Installer runtime source | `255ee2053a80f008fc5e422b4f9ac8e9bcc53618` |

SHA-256:

```text
c026c48c7bd2775c79af03dfadfd432b4166d96516667511b80febb3915c4f46
```

Six package versions are prepared for this release: Calamares 3.4.2.23,
settings 1.5.13, desktop-utils 1.0.6, xinit 1.4.4.6, XLibre server 25.1.9.1
and dinit services 0.1.14. Preparation is not binary publication.

### Exact-image qualification

| Check | Status on the combined image |
| --- | --- |
| Pinned inputs, embedded files, package databases and runtime libraries | Passed; independent actual-ISO audit verifies both settings helpers and the target-only readiness helper/service. |
| Source checks | 50 settings tests, four readiness tests, configuration checks, 41 toolkit tests and seven unchanged native installer suites passed. |
| Minimum root and EFI size | Passed: actual 12,801 MiB root / 64 MiB ESP install, full original-partition preservation, both Linux boot choices, two normal-user desktops, restart and shutdown. |
| 1024×768 workflow | Passed: explicit choices, invalid-input and keyboard validation, Summary/Back/Revert; no writes before confirmed Install. |
| Empty drive | Passed: blank 32 GiB disk, 512 MiB ESP, remaining-space root, disk-only normal-user desktop and authenticated shutdown. |
| Genuine Windows | Passed: Easy install, Expert reinstall, original GPT/data partitions and 146 EFI files preserved, both desktops, no duplicate firmware entry and normal evaluation activation. |
| Protected BitLocker | Passed: encrypted partitions and EFI files preserved, controlled recovery, post-install resealing and subsequent protected Windows boot without another recovery prompt. |
| 4Kn and multiple ESPs | Passed: 4Kn target, second region/second ESP, 16 GiB root, two normal-user desktop boots, preserved partitions and neighbors, zero-write stale/altered-plan refusal and read-only dirty-FAT rejection. |

These rows refer only to the SHA-256 above. Earlier November 5, settings
1.5.11 and settings 1.5.12 images were rejected; their passing subtests do
not qualify changed image bytes.

### What testing found

- Windows Setup leaves a harmless mismatch between two FAT EFI volume-label
  fields. The read-only preflight now accepts only that precise label-only
  diagnostic and continues to reject dirty filesystems and other errors.
- An old Tuxenix loader on another ESP must remain in the new menu even when
  the selected ESP initially has no EFI directory. Tests now inspect both
  the first installation and a repeat installation.
- Starting the udev process did not guarantee it was ready for device events.
  The installed boot graph now waits for a control reply with a 30-second
  deadline, then triggers and settles devices. Failure stops the trigger.

See the [engineering notes](engineering.md) for the causes and focused tests.

### Windows and BitLocker scope

The fixture is genuine Windows 11 Enterprise Evaluation 26H2 build
26300.9457, UEFI/GPT, with ESP, MSR, Windows and enabled WinRE. Preservation
compares complete existing data partitions and all 146 foreign EFI files
before normal Windows startup, which legitimately changes filesystem bytes.

BitLocker tests use a software TPM2, XTS-AES128 used-space-only encryption,
100% encryption and protection On. The final combined image was tested with protection On at installation.
The first Windows boot through Limine requested the controlled recovery key.
Recovery succeeded. Suspending protection, booting Windows through
Limine, resuming protection and booting through the same entry again produced
a protected boot without another prompt. That sequence passed on the exact combined image. Suspension before
installation was not tested; this is not a guarantee of prompt-free startup
on other hardware. Recovery material is private and is never included in these docs.

Secure Boot, hardware TPM, physical graphics/Wi-Fi/audio, games and suspend
remain outside this image's qualification. These are specific test limits,
not evidence that all such hardware fails. Tuxenix root encryption, LVM/RAID
installation targets and automatic filesystem shrinking are not implemented
by this alongside workflow.

## Source integration

The current review requests are [package MR !5](https://gitlab.anysolo.com/opensource/anysolo-linux/pkg-sources/-/merge_requests/5)
and [installer MR !3](https://gitlab.anysolo.com/opensource/anysolo-linux/installer/-/merge_requests/3).
The package branch is `feature/easy-dual-boot-2026-11-05`; the installer MR
uses `tuxenix-steam-publication`. Package main already contains the older
October 30 review; the new release changes still require administrator-approved
protected merges. The existing requests contain the final source, qualification
and website records; keep using those requests rather than opening duplicates.

The release procedure requires the tested source to be present in main,
reviewed package/site staging and complete HTTPS readback of the published
ISO and changed files. The project page will not describe a local build,
Git push or prepared upload as a verified public release.

## Published image: October 22

[Download the published image](https://tuxenix.org/iso/tuxenix-dinit-desktop-2026-10-22.iso)
and [its checksum](https://tuxenix.org/iso/tuxenix-dinit-desktop-2026-10-22.iso.sha256).
Size: 1,313,968,128 bytes. SHA-256:

```text
8ae76d8d70ffc346c675ba66cbea269b6d2bb9f470c9f94b43e0a5cd9286fc9e
```

That image uses Calamares 3.4.2.16/settings 1.5.8 and the October 17 system
payload. Its original tests and the superseded October 30 candidate remain
in the [historical status record](status-2026-10-30.md), with their own
artifacts, hashes and limits. The [getting-started guide](getting-started.md)
continues to describe the published image until the new release is verified.

`power-utils` 1.0.0 was separately published October 29 and remains available
with `sudo txpk --install power-utils`. Package releases and ISO releases
have independent dates.

## Next work and release handoff

1. Complete administrator-approved protected source merges for package MR !5
   and installer MR !3. All required exact-image tests and website review have
   passed; protected merges are the remaining release gate. Verify that the
   reviewed source and required runtime commits are in main before deployment.
2. Capture a fresh public baseline and prepare a new release staging directory.
   The status-only website publication changed the earlier baseline, so the
   old full-release upload plan must not be reused. Keep the exact qualified
   ISO bytes identified above; do not rebuild without requalifying the result.
3. Before deployment, download the public October 22 ISO into a temporary
   rollback workspace and verify its size and SHA-256 above. Only the final
   candidate is retained locally after the requested cleanup; older local ISO
   files were removed. Publish the dated ISO and six package versions, preserve
   existing published archives and the previous public ISO, and verify every changed
   public file over HTTPS before calling the replacement released. Then update
   this status and the published-image guide. Remove the temporary local
   rollback copy after verified completion.
4. Collect dated physical hardware results for the remaining coverage gaps.

All owned qualification VMs are stopped. Preserve test records and original
fixture bases, keep recovery material private, and leave the working laptop
untouched. Historical reports and manifests identify earlier images; their
presence does not imply those ISO files remain stored locally.

[Report hardware results](https://github.com/elgun-dev/Tuxenix/issues/new?template=hardware-report.yml)

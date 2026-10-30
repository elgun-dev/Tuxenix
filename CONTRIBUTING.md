# Contributing to Tuxenix

Useful contributions make a problem reproducible, clarify an installation
step or establish what works on a specific machine.

## Report a failure

Use the [bug form](https://github.com/elgun-dev/Tuxenix/issues/new?template=bug-report.yml).
Include the ISO filename/date, any packages updated afterward, the hardware
or VM configuration, and whether the failure is in the live or installed
system. Describe the last successful step, the exact command or action that
failed, and what you expected to happen.

Attach the complete error output where possible. For installation failures,
include the page or job that failed and the bootloader dialog's underlying
command output. For package failures, include the package name, version and
command. Remove passwords, tokens and personal network details from logs.
Do not post NetworkManager connection files containing credentials.

## Report hardware results

Use the [hardware form](https://github.com/elgun-dev/Tuxenix/issues/new?template=hardware-report.yml)
for working systems as well as failures. Identify the machine, GPU, network
adapter, image date, kernel and later package updates. Separate observations:
booting the desktop, connecting Wi-Fi, playing audible sound, suspending and
running a game are different tests.

A VM report should name the virtual devices and firmware. Software rendering
is useful evidence, but it is not a physical GPU result. An untested feature
should stay marked untested rather than inherit the rest of the machine's result.

## Documentation changes

Open a pull request against this repository. Explain the incorrect or missing
step and the evidence for the replacement. Use conventional command names,
copyable examples and links to the relevant dated release.

Keep [the overview](README.md), [getting started](docs/getting-started.md) and
[release status](docs/status.md) consistent. Add dated milestones to the
[progress log](docs/progress.md) and its README timeline. When recording a release:

- Use the dated artifact URL, exact size and SHA-256.
- Identify which tests used the final artifact and which used an earlier build.
- Keep historical results attached to their original image and hardware.
- Separate source changes, published packages and published images.
- Update the copied package manifest only from the corresponding release record.

Before submitting, check relative links, code-block commands and table layout.
For screenshots, include the image date and test context. Avoid capturing
credentials or using an unreleased interface to illustrate the current image.

## Package or installer code

The build trees are listed in the [source map](docs/architecture.md#source-map).
Access may require GitLab sign-in. Code changes belong in the appropriate
source repository; this GitHub repository is an overview and issue tracker.
If you cannot access the source host, a report here can still describe the
problem and include a focused diff.

Record the source revision, package versions, archive hashes and validation
for a code change. An installer change needs evidence from a finished image;
a successful package build alone does not establish that installation works.

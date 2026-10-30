# Tuxenix RAM Monitor dinit service

This is a standalone dinit service, not a software package. Its Bash daemon
records current RAM use immediately after starting and once every 60 seconds.

## Install

From this directory on Tuxenix:

```sh
sudo ./install.sh
```

The installer copies the daemon to `/usr/local/libexec`, installs the viewer
under `/usr/local/bin`, installs the dinit service in `/etc/dinit.d`, and
creates this automatic-boot link:

```text
/etc/dinit.d/boot.d/tuxenix-ram-monitor -> ../tuxenix-ram-monitor
```

If dinit is already running as PID 1, the installer also starts the service
immediately. Otherwise it starts automatically at the next dinit boot.

## Use

Show the latest reading:

```sh
tuxenix-ram-usage
```

The underlying status file is:

```text
/run/tuxenix-ram-monitor/status
```

Manage or inspect the service with:

```sh
dinitctl status tuxenix-ram-monitor
dinitctl catlog tuxenix-ram-monitor
dinitctl restart tuxenix-ram-monitor
dinitctl stop tuxenix-ram-monitor
dinitctl start tuxenix-ram-monitor
```

The status file is updated atomically, so readers never see a partially
written sample. Recent service output stays in dinit's bounded memory log
instead of accumulating forever in `/var/log`.

## Uninstall

```sh
sudo ./uninstall.sh
```

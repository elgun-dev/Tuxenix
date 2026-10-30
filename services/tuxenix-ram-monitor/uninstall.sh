#!/bin/bash

set -euo pipefail

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PATH

destination_root="${DESTDIR:-}"
service_name=tuxenix-ram-monitor

if [[ -z "${destination_root}" ]] && (( EUID != 0 )); then
  echo "Run this uninstaller as root: sudo ./uninstall.sh" >&2
  exit 1
fi

if [[ -z "${destination_root}" ]] &&
   [[ -r /proc/1/comm ]] &&
   [[ "$(< /proc/1/comm)" == dinit ]] &&
   command -v dinitctl >/dev/null 2>&1; then
  dinitctl stop --ignore-unstarted "${service_name}" || true
  dinitctl unload "${service_name}" || true
fi

rm -f \
  "${destination_root}/etc/dinit.d/boot.d/tuxenix-ram-monitor" \
  "${destination_root}/etc/dinit.d/tuxenix-ram-monitor" \
  "${destination_root}/usr/local/bin/tuxenix-ram-usage" \
  "${destination_root}/usr/local/libexec/tuxenix-ram-monitor"

if [[ -z "${destination_root}" ]]; then
  rm -f /run/tuxenix-ram-monitor/status
  rmdir /run/tuxenix-ram-monitor 2>/dev/null || true
fi

echo "Removed ${service_name}."

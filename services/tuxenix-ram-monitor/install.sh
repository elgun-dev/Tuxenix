#!/bin/bash

set -euo pipefail

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PATH

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
destination_root="${DESTDIR:-}"
service_name=tuxenix-ram-monitor

if [[ -z "${destination_root}" ]] && (( EUID != 0 )); then
  echo "Run this installer as root: sudo ./install.sh" >&2
  exit 1
fi

install -Dm755 \
  "${script_dir}/ram-monitor.sh" \
  "${destination_root}/usr/local/libexec/tuxenix-ram-monitor"

install -Dm755 \
  "${script_dir}/ram-usage.sh" \
  "${destination_root}/usr/local/bin/tuxenix-ram-usage"

install -Dm644 \
  "${script_dir}/tuxenix-ram-monitor" \
  "${destination_root}/etc/dinit.d/tuxenix-ram-monitor"

install -d -m 0755 "${destination_root}/etc/dinit.d/boot.d"
ln -sfn ../tuxenix-ram-monitor \
  "${destination_root}/etc/dinit.d/boot.d/tuxenix-ram-monitor"

if [[ -n "${destination_root}" ]]; then
  echo "Staged ${service_name} under ${destination_root}."
  exit 0
fi

if command -v dinit-check >/dev/null 2>&1; then
  dinit-check -d /etc/dinit.d "${service_name}"
fi

if [[ -r /proc/1/comm ]] &&
   [[ "$(< /proc/1/comm)" == dinit ]] &&
   command -v dinitctl >/dev/null 2>&1; then
  dinitctl reload "${service_name}" >/dev/null 2>&1 || true

  if dinitctl --quiet is-started "${service_name}"; then
    dinitctl restart "${service_name}"
  else
    dinitctl start "${service_name}"
  fi

  echo "Installed, enabled, and started ${service_name}."
else
  echo "Installed and enabled ${service_name}; it will start at the next dinit boot."
fi

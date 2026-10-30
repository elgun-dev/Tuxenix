#!/bin/bash

set -euo pipefail

status_file="${TUXENIX_RAM_STATUS_FILE:-/run/tuxenix-ram-monitor/status}"

if [[ ! -r "${status_file}" ]]; then
  echo "No RAM status is available yet." >&2
  echo "Check the service with: dinitctl status tuxenix-ram-monitor" >&2
  exit 1
fi

cat "${status_file}"

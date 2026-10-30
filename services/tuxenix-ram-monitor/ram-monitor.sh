#!/bin/bash

set -euo pipefail

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LC_ALL=C
export PATH LC_ALL

interval_seconds="${TUXENIX_RAM_INTERVAL_SECONDS:-60}"
meminfo_file="${TUXENIX_RAM_MEMINFO_FILE:-/proc/meminfo}"
status_dir="${TUXENIX_RAM_STATUS_DIR:-/run/tuxenix-ram-monitor}"
status_file="${status_dir}/status"
temporary_status="${status_file}.tmp.$$"

if [[ ! "${interval_seconds}" =~ ^[1-9][0-9]*$ ]]; then
  echo "tuxenix-ram-monitor: interval must be a positive whole number" >&2
  exit 2
fi

cleanup() {
  rm -f "${temporary_status}"
}

stop() {
  exit 0
}

trap cleanup EXIT
trap stop INT TERM

read_memory() {
  local key value ignored
  local total_kib=0
  local available_kib=0
  local free_kib=0
  local buffers_kib=0
  local cached_kib=0

  while read -r key value ignored; do
    case "${key}" in
      MemTotal:)     total_kib="${value}" ;;
      MemAvailable:) available_kib="${value}" ;;
      MemFree:)      free_kib="${value}" ;;
      Buffers:)      buffers_kib="${value}" ;;
      Cached:)       cached_kib="${value}" ;;
    esac
  done < "${meminfo_file}"

  if (( total_kib <= 0 )); then
    echo "tuxenix-ram-monitor: could not read MemTotal from ${meminfo_file}" >&2
    return 1
  fi

  if (( available_kib <= 0 )); then
    available_kib=$((free_kib + buffers_kib + cached_kib))
  fi

  if (( available_kib > total_kib )); then
    available_kib="${total_kib}"
  fi

  local used_kib=$((total_kib - available_kib))
  local used_mib=$(((used_kib + 512) / 1024))
  local available_mib=$(((available_kib + 512) / 1024))
  local total_mib=$(((total_kib + 512) / 1024))
  local usage_tenths=$((used_kib * 1000 / total_kib))
  local usage_whole=$((usage_tenths / 10))
  local usage_decimal=$((usage_tenths % 10))
  local timestamp

  timestamp="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

  printf '%s RAM: %d MiB used / %d MiB total (%d.%d%%), %d MiB available' \
    "${timestamp}" \
    "${used_mib}" \
    "${total_mib}" \
    "${usage_whole}" \
    "${usage_decimal}" \
    "${available_mib}"
}

mkdir -p "${status_dir}"
chmod 0755 "${status_dir}"
umask 0022

while true; do
  sample="$(read_memory)"
  printf '%s\n' "${sample}" > "${temporary_status}"
  chmod 0644 "${temporary_status}"
  mv -f "${temporary_status}" "${status_file}"
  printf '%s\n' "${sample}"
  sleep "${interval_seconds}"
done

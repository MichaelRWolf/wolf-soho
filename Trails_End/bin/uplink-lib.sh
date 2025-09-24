#!/usr/bin/env bash
set -euo pipefail

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dep: $1" >&2; exit 1; }; }
need curl
need jq
need ipcalc
need traceroute

get_public_ip() { curl -s https://ifconfig.me; }

get_org_from_rdap() {
  local ip="$1" rdap
  rdap="$(curl -s "https://rdap.arin.net/registry/ip/${ip}")"
  jq -r '(
      .entities // []
      | map(select(.roles[]? | test("registrant|administrative")))
      | .[0]?.vcardArray[1][]?
      | select(.[0]=="fn") | .[3]
    ) // .name // "Unknown"
  ' <<<"$rdap"
}

is_cgnat_ipv4() {
  local ip="$1"
  [[ "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || return 1
  ipcalc -nb 100.64.0.0/10 "$ip" >/dev/null 2>&1
}

uplink_description_short() {
  local ip org nat="public IP"
  ip="$(get_public_ip)"
  org="$(get_org_from_rdap "$ip")"
  if is_cgnat_ipv4 "$ip"; then nat="CGNAT (shared IPv4)"; fi
  echo "Uplink: ${org} — ${nat} — IP ${ip}"
}

uplink_description_verbose() {
  echo "=== $(date '+%F %T') ==="
  uplink_description_short
  echo
  traceroute -n -m 6 1.1.1.1
  echo
}

uplink_log_loop() {
  local log="${1:-$HOME/uplink_log.txt}"
  local sec="${2:-300}"
  while true; do
    { uplink_description; } >> "$log"
    sleep "$sec"
  done
}

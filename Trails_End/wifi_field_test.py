#!/usr/bin/env python3
"""WiFi field test script: logs RSSI, ping, and connection data to JSONL.

Infers antenna/site from connected BSSID when possible; requires manual --computer
and (when necessary) --eap location for wandering EAP225 repeater.
"""

import argparse
import dataclasses
import datetime
import json
import pathlib
import platform
import re
import subprocess
import sys
from typing import Optional

SCRIPT_DIR = pathlib.Path(__file__).parent
JSONL_PATH = SCRIPT_DIR / "wifi_field_test.jsonl"
TEST_HOST = "8.8.8.8"
PING_COUNT = 20

KNOWN_BSSIDS = {
    # Trails End fixed sites — each broadcasts 3 SSIDs (Trails End Wifi / Trails End Crew /
    # Lake Effect Farm) off the same radio; full detail in Trails_End/network_topology.md
    "74:ac:b9:cb:36:38": {"name": "Welcome Antenna", "kind": "trails_end"},
    "7a:ac:b9:cb:36:38": {"name": "Welcome Antenna", "kind": "trails_end"},
    "7e:ac:b9:cb:36:38": {"name": "Welcome Antenna", "kind": "trails_end"},
    "74:ac:b9:ca:36:38": {"name": "Welcome Antenna", "kind": "trails_end"},
    "7a:ac:b9:ca:36:38": {"name": "Welcome Antenna", "kind": "trails_end"},
    "74:ac:b9:cb:3b:c1": {"name": "Barn North Antenna", "kind": "trails_end"},
    "7a:ac:b9:cb:3b:c1": {"name": "Barn North Antenna", "kind": "trails_end"},
    "7e:ac:b9:cb:3b:c1": {"name": "Barn North Antenna", "kind": "trails_end"},
    "74:ac:b9:ca:3b:c1": {"name": "Barn North Antenna", "kind": "trails_end"},
    "7a:ac:b9:ca:3b:c1": {"name": "Barn North Antenna", "kind": "trails_end"},
    "7e:ac:b9:ca:3b:c1": {"name": "Barn North Antenna", "kind": "trails_end"},
    "f4:e2:c6:24:b3:a1": {"name": "Unconfirmed Site (:A1)", "kind": "trails_end"},
    "fa:e2:c6:24:b3:a1": {"name": "Unconfirmed Site (:A1)", "kind": "trails_end"},
    "fe:e2:c6:24:b3:a1": {"name": "Unconfirmed Site (:A1)", "kind": "trails_end"},
    # "TODO-fill-in": {"name": "Barn Equipment Panel", "kind": "trails_end"},
    "94:83:c4:11:9c:da": {"name": "Beryl (RV)", "kind": "wolf"},
    # "TODO-fill-in": {"name": "Beryl (RV) 2.4GHz", "kind": "wolf"},
    "18:69:45:38:a2:f2": {"name": "EAP225", "kind": "eap"},
    "18:69:45:38:a2:f3": {"name": "EAP225", "kind": "eap"},
}


@dataclasses.dataclass
class NetworkInfo:
    ssid: str
    bssid: str
    rssi: int


@dataclasses.dataclass
class PingStats:
    host: str
    count: int
    avg_ms: float
    min_ms: float
    max_ms: float
    stddev_ms: float
    packet_loss_pct: float


def warn(msg: str) -> None:
    print(f"❌ Error: {msg}", file=sys.stderr)


def get_current_network_info() -> Optional[NetworkInfo]:
    """Parse airport -I output to extract SSID, BSSID, RSSI."""
    airport_path = (
        "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/"
        "Current/Resources/airport"
    )
    try:
        result = subprocess.run(
            [airport_path, "-I"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        warn(f"airport -I failed: {e}")
        return None

    ssid = None
    bssid = None
    rssi = None

    for line in result.stdout.split("\n"):
        if "SSID:" in line:
            ssid = line.split("SSID:")[1].strip()
        elif "BSSID:" in line:
            bssid = line.split("BSSID:")[1].strip()
        elif "agrCtlRSSI:" in line:
            try:
                rssi = int(line.split("agrCtlRSSI:")[1].strip())
            except (ValueError, IndexError):
                pass

    if not ssid or not bssid or rssi is None:
        return None

    return NetworkInfo(ssid=ssid, bssid=bssid, rssi=rssi)


def run_ping(host: str, count: int) -> Optional[PingStats]:
    """Run ping and extract latency/jitter/loss stats."""
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "1000", host],
            capture_output=True,
            text=True,
            timeout=count * 2,
        )
    except subprocess.TimeoutExpired:
        warn(f"ping {host} timed out")
        return None

    lines = result.stdout.split("\n")
    if not lines:
        return None

    summary_line = lines[-2] if len(lines) > 1 else ""

    # Extract: min/avg/max/stddev = X/Y/Z/W ms
    match = re.search(r"= ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms", summary_line)
    if not match:
        warn(f"Could not parse ping summary: {summary_line}")
        return None

    min_ms, avg_ms, max_ms, stddev_ms = [float(x) for x in match.groups()]

    # Extract packet loss %
    loss_match = re.search(r"([\d.]+)% packet loss", summary_line)
    packet_loss_pct = float(loss_match.group(1)) if loss_match else 0.0

    return PingStats(
        host=host,
        count=count,
        avg_ms=avg_ms,
        min_ms=min_ms,
        max_ms=max_ms,
        stddev_ms=stddev_ms,
        packet_loss_pct=packet_loss_pct,
    )


def load_last_record() -> Optional[dict]:
    """Load the last JSON record from the JSONL file."""
    if not JSONL_PATH.exists():
        return None
    try:
        with open(JSONL_PATH) as f:
            lines = [line.strip() for line in f if line.strip()]
        return json.loads(lines[-1]) if lines else None
    except (json.JSONDecodeError, IOError):
        return None


def resolve_site(bssid: str, cli_eap: Optional[str]) -> dict:
    """Resolve the site name from BSSID or manual --eap input."""
    if cli_eap:
        return {
            "name": cli_eap,
            "bssid": bssid,
            "kind": "eap",
            "source": "manual",
        }

    bssid_lower = bssid.lower()
    if bssid_lower in KNOWN_BSSIDS:
        entry = KNOWN_BSSIDS[bssid_lower]
        return {
            "name": entry["name"],
            "bssid": bssid,
            "kind": entry["kind"],
            "source": "auto",
        }

    # Unrecognized BSSID: try reuse-if-recent, else require manual
    last_record = load_last_record()
    if last_record:
        ts_str = last_record.get("timestamp", "")
        try:
            ts = datetime.datetime.fromisoformat(ts_str)
            age = datetime.datetime.now(datetime.timezone.utc) - ts.replace(
                tzinfo=datetime.timezone.utc
            )
            if age.total_seconds() < 300:  # 5 min
                return last_record.get("eap", {})
        except (ValueError, TypeError):
            pass

    # No recent log and BSSID not recognized
    print(
        f"⚠️  BSSID {bssid} not recognized — consider adding it to KNOWN_BSSIDS",
        file=sys.stderr,
    )
    return {
        "name": None,
        "bssid": bssid,
        "kind": "unknown",
        "source": "manual",
    }


def main():
    parser = argparse.ArgumentParser(
        description="WiFi field test: log RSSI, ping, connection data to JSONL.",
        epilog="""
Antenna Reference (fixed positions):
  • Welcome Antenna (:38)       — 0 ft, primary outdoor (channels 36, 44)
  • Barn North Antenna (:C1)    — 200 ft, bearing 45° (outdoor ridge, north roof)
  • Barn Equipment Panel (:93)  — 227 ft, bearing 15° (inside barn, north window)

Examples:
  %(prog)s --computer "Picnic Table"
  %(prog)s --computer "Welcome Antenna area" --eap "Barn North (repeater)"
  %(prog)s --computer "Test A" --repeater-bssid "7e:ac:b9:cb:36:38"
        """,
    )
    parser.add_argument(
        "--computer",
        help="Laptop's physical location (free text)",
    )
    parser.add_argument(
        "--eap",
        help="EAP225's current position (free text, e.g., 'Picnic Table')",
    )
    parser.add_argument(
        "--repeater-bssid",
        help="Trails End BSSID the EAP225 bridges from (optional)",
    )

    args = parser.parse_args()

    # Check WiFi connection
    net_info = get_current_network_info()
    if not net_info:
        warn(
            "Not connected to WiFi or airport -I failed. Connect first, then try again."
        )
        sys.exit(1)

    print("╔════════════════════════════════════════╗")
    print("║  WiFi Field Test — Currently On:       ║")
    print("╚════════════════════════════════════════╝")
    print(f"SSID:  {net_info.ssid}")
    print(f"BSSID: {net_info.bssid}")
    print(f"RSSI:  {net_info.rssi} dBm")
    print()

    # Resolve --computer (required)
    computer = args.computer
    if not computer:
        last = load_last_record()
        if last and last.get("computer"):
            ts_str = last.get("timestamp", "")
            try:
                ts = datetime.datetime.fromisoformat(ts_str)
                age = datetime.datetime.now(datetime.timezone.utc) - ts.replace(
                    tzinfo=datetime.timezone.utc
                )
                if age.total_seconds() < 300:
                    computer = last["computer"]
            except (ValueError, TypeError):
                pass

    if not computer:
        warn("--computer location required")
        parser.print_help()
        sys.exit(1)

    # Resolve site/EAP from BSSID
    site = resolve_site(net_info.bssid, args.eap)
    if not site["name"]:
        warn("Could not determine EAP location. Use --eap 'location'")
        sys.exit(1)

    # Run ping
    print("Testing latency/jitter (20 pings)...")
    ping_stats = run_ping(TEST_HOST, PING_COUNT)
    if not ping_stats:
        warn(f"Ping to {TEST_HOST} failed")
        sys.exit(1)

    # Assemble and append record
    record = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "hostname": platform.node(),
        "computer": computer,
        "eap": site,
        "repeater_bssid": args.repeater_bssid,
        "network": {
            "SSID": net_info.ssid,
            "BSSID": net_info.bssid,
            "agrCtlRSSI": net_info.rssi,
        },
        "ping": {
            "host": TEST_HOST,
            "count": PING_COUNT,
            "avg_ms": ping_stats.avg_ms,
            "min_ms": ping_stats.min_ms,
            "max_ms": ping_stats.max_ms,
            "stddev_ms": ping_stats.stddev_ms,
            "packet_loss_pct": ping_stats.packet_loss_pct,
        },
        "speedtest": None,
    }

    with open(JSONL_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

    # Display results
    print()
    print(f"═══ Results for: {computer} ═══")
    print(f"Network:         {net_info.ssid}")
    print(f"Site:            {site['name']} ({site['kind']})")
    print(f"RSSI:            {net_info.rssi} dBm")
    print(f"Latency (avg):   {ping_stats.avg_ms}ms")
    print(f"Latency (min):   {ping_stats.min_ms}ms")
    print(f"Latency (max):   {ping_stats.max_ms}ms")
    print(f"Jitter (stddev): {ping_stats.stddev_ms}ms")
    print(f"Packet Loss:     {ping_stats.packet_loss_pct}%")
    print()
    print(f"✓ Appended to: {JSONL_PATH}")
    print()
    print("Next: Move EAP, connect to network, run again.")


if __name__ == "__main__":
    main()

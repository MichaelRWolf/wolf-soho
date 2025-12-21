#!/bin/sh
# uci_set_country.sh
# Set GL.iNet Beryl (GL-MT1300) Wi-Fi regulatory domain to US and reload Wi-Fi.
# Intended to be run ON the router after SSH login (as root).
set -eu

if [ "$(id -u)" != "0" ]; then
  echo "ERROR: must run as root (on OpenWrt/GL.iNet router)."
  exit 1
fi

echo "==> Setting UCI country/region/regdom to US (MT7615)"
# These names matched your device: wireless.mt7615e5 and wireless.mt7615e2
# country: used by OpenWrt config
# region/aregion: MediaTek driver-specific regulatory settings (important on MT7615)
uci set wireless.mt7615e5.country='US' || true
uci set wireless.mt7615e2.country='US' || true

# US region values observed/used on MT7615: region 7, aregion 10
uci set wireless.mt7615e5.region='7' || true
uci set wireless.mt7615e5.aregion='10' || true
uci set wireless.mt7615e2.region='7' || true
uci set wireless.mt7615e2.aregion='10' || true

# Global regdomain hint (may or may not be honored by driver; harmless to set)
uci set wireless.regdom='US' || true

echo "==> Committing UCI changes"
uci commit wireless

echo "==> Setting kernel regdomain to US (runtime)"
iw reg set US || true

echo "==> Reloading Wi-Fi"
wifi reload || true

echo "==> Verifying kernel regdomain"
iw reg get || true

echo "==> Showing configured wireless country/region/regdom"
uci show wireless | grep -E "country|regdom|region|aregion" || true

echo "==> Done."

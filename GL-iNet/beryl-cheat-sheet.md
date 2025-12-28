# yad yada

## From Raw uci commands

via `ssh root@beryl`

### Beryl

`uci show  network.lan`

network.lan=interface
network.lan.type='bridge'
network.lan.ifname='eth0.1'
network.lan.proto='static'
network.lan.netmask='255.255.255.0'
network.lan.ip6assign='60'
network.lan.hostname='GL-MT1300-cd7'
network.lan.ipaddr='192.168.8.1'
network.lan.multicast_to_unicast='0'

### Nighthawk

`uci show wireless.sta`

wireless.sta=wifi-iface
wireless.sta.network='wwan'
wireless.sta.mode='sta'
wireless.sta.ifname='apclix0'
wireless.sta.ssid='Running Wolf Hot Spot'
wireless.sta.bssid='44:A5:6E:E9:59:25'
wireless.sta.channel='7'
wireless.sta.device='mt7615e2'
wireless.sta.encryption='psk2'
wireless.sta.key='29U926gC'

### NAS

`uci show dhcp.001132EA251B`

dhcp.001132EA251B=host
dhcp.001132EA251B.mac='00:11:32:EA:25:1B'
dhcp.001132EA251B.ip='192.168.8.129'

## From ChatGPT

### LAN IP

192.168.8.1

### SSIDs

wireless.wifi5g.ssid='Running Wolf Router - 5G'
wireless.wifi2g.ssid='Running Wolf Router'
wireless.guest5g.ssid='Running Wolf Guest - 5G'
wireless.guest2g.ssid='Running Wolf Guest'
wireless.sta.ssid='Running Wolf Hot Spot'

### WiFi Keys

wireless.wifi5g.key='Since1995!'
wireless.wifi2g.key='Since1995!'
wireless.guest5g.key='Tam&LindaRock!'
wireless.guest2g.key='Visiting2RWolf!'
wireless.sta.key='29U926gC'

### DHCP Static Leases

dhcp.localhost.name='console.gl-inet.com'
dhcp.localhost.ip='192.168.8.1'

dhcp.001132EA251B=host
dhcp.001132EA251B.mac='00:11:32:EA:25:1B'
dhcp.001132EA251B.ip='192.168.8.129'

dhcp.001132EA251B.mac='00:11:32:EA:25:1B'
dhcp.001132EA251B.ip='192.168.8.129'

## Password-less SSH (Post-Reset)

After factory reset, re-enable key-based SSH once from each client.

```sh
# first login (password)
ssh root@192.168.8.1

# on Beryl
mkdir -p /root/.ssh && chmod 700 /root/.ssh

# from each Mac
ssh-copy-id root@192.168.8.1

# back on Beryl
chmod 600 /root/.ssh/authorized_keys
```

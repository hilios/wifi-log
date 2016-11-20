# WiFi APC

### Automatic passengers count through WiFi signal

A simple command line utility to count people in the area of a WiFi antena.

To run ensure your wireless interface is set to the promiscuous mode:

```bash
$ airmon-ng start wlan0
$ ifconfig
# ...
wlan0mon  Link encap:UNSPEC  HWaddr 00-0C-13-15-10-70-30-30-00-00-00-00-00-00-00-00
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:33 errors:0 dropped:33 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:4599 (4.4 KiB)  TX bytes:0 (0.0 B)
```

Then run the

```bash
$ wifi-apc wlan0mon
```

You can control several aspects of the execution by parameters:

```bash
# Publish monitoring output to port 8888 trough ØMQ
$ wifi-apc -P 8888 wlan0 wlan0mon
# Log to file
$ wifi-apc -l log.txt wlan0 wlan0mon
```

More info at `wifi-apc --help`.

## Installing

This software uses the [aircrack-ng](https://www.aircrack-ng.org/) tool to setup the promiscuous mode, to install at a Raspberry Pi follow the steps:

```sh
sudo apt-get -y install libssl-dev libnl-dev

# Install aircrack-ng
wget http://download.aircrack-ng.org/aircrack-ng-1.2-rc4.tar.gz
tar -zxvf aircrack-ng-1.2-rc4.tar.gz
cd aircrack-ng-1.2-rc4
# Build & install
make
sudo make install
sudo airodump-ng-oui-update # May take a while
```

Then install this package

```
$ pip install --editable .
```

## Monitoring via Wireshark

This application does the same job as Tshark (Wireshark's CLI app), to check the output you can:

```bash
$ sudo apt-get -y install tshark
$ tshark -i wlan0mon -n -l -Y "wlan.fc.type_subtype==4"
```

## More about 802.11

- https://en.wikipedia.org/wiki/IEEE_802.11#Management_frames

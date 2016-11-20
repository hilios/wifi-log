# WiFi APC

### Automatic passengers count through WiFi signal

A simple command line utility to count people in the area of a WiFi antena.

Set the promiscuous mode at the wireless interface:

```bash
sudo apt-get -y install iw
airmon-ng start wlan0
airodump-ng mon0 # Start monitor mode at mon0 interface
```

```bash
$ pip install -e .
$ wifi-apc wlan0 wlan0mon
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

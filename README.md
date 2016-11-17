# WiFi APC

### Automatic passengers count through WiFi signal

A simple command line utility to count people around some device with a WiFi antena in monitor mode.

```
$ pip install -e .
$ wifi-apc
```

## Requirements

```sh
sudo apt-get -y install libssl-dev libnl-3-dev

# Install aircrack-ng
wget http://download.aircrack-ng.org/aircrack-ng-1.2-rc4.tar.gz
tar -zxvf aircrack-ng-1.2-rc4.tar.gz
cd aircrack-ng-1.2-rc4
# Build & install
make
sudo make install
sudo airodump-ng-oui-update
```

Set the promiscuous mode at the wireless interface:

```bash
sudo apt-get -y install iw
airmon-ng start wlan0
airodump-ng mon0 # Start monitor mode at mon0 interface
```

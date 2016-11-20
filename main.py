"""A command line interface to monitor 802.11 network probe requests.
Usage:
    $ wifi-apc wlan0mon

For more info type:
    $ wifi-apc -h
"""
import argparse
import logging
import json
import os
import sys
import zmq


if os.geteuid() != 0:
    print >> sys.stderr, "You need root permissions to run this program."
    sys.exit(1)


def monitor(iface, port):
    "Monitors the interface for probe requests."
    try:
        from scapy.all import sniff, Dot11ProbeReq, Dot11ProbeResp, Dot11
    except ImportError:
        print >> sys.stderr, "Did you install all the packager requirements?"
        sys.exit(1)

    log = logging.getLogger(__name__)

    # Open socket
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    def handler(pkt):
        "Parses each package captured and publishes to log and socket."
        if pkt.haslayer(Dot11) :
            info = {'mac_address': pkt.addr2.upper(), 'ssid': pkt.info}
            log.info("Device MAC: %(mac_address)s with SSID: %(ssid)s" % info)
            socket.send(json.dumps(info))

    log.info("Monitoring network `%s` publishing at *:%s" % (iface, port))

    sniff(iface=iface, prn=handler, store=False,
        lfilter=lambda p: p.haslayer(Dot11ProbeReq))


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--port', '-P', action='store', type=int, default=5555)
    parser.add_argument('--log-file', '-l', type=argparse.FileType('w+'))
    parser.add_argument('iface', action='store', help="the interface to monitor")
    args = parser.parse_args()
    # Configure log utility
    logging.basicConfig(format="%(asctime)-15s\t%(levelname)-5s\t%(message)s",
        level=logging.INFO if not args.verbose else logging.DEBUG)
    # Start monitoring
    monitor(args.iface, args.port)


if __name__ == "__main__":
    run()

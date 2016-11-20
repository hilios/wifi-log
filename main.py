"""A command line interface to monitor 802.11 network probe requests.
Usage:
    $ wifi-apc wlan0 wlan0mon

For more info type:
    $ wifi-apc -h

To monitor via Wireshark:
    $ tshark -i wlan0mon -n -l -Y "wlan.fc.type_subtype==4"
"""
import logging
import json
import os
import sys
import zmq


if os.geteuid() != 0:
    print >> sys.stderr, "You need root permissions to run this program."
    sys.exit(1)


def monitor(iface, miface, socket, log):
    "Sniff  the given interface for probe requests."
    try:
        from scapy.all import sniff, Dot11ProbeReq, Dot11ProbeResp, Dot11
        from sh import sudo, airmon_ng, ErrorReturnCode
        sudo.airmon_ng('check', 'kill')
        sudo.airmon_ng('start', iface)
    except ImportError:
        print >> sys.stderr, "Did you install all the packager requirements?"
        sys.exit(1)
    except ErrorReturnCode:
        print >> sys.stderr, "Your system does not support sniffing."
        sys.exit(1)

    def handler(pkt):
        if pkt.haslayer(Dot11) :
            info = {'mac_address': pkt.addr2, 'ssid': pkt.info}
            socket.send(json.dumps(info))
            log.info("AP MAC: %(mac_address)s with SSID: %(ssid)s".format(info))

    log.info("Monitoring network %s" % iface)

    sniff(iface=iface, prn=handler, store=False,
        lfilter=lambda p: p.haslayer(Dot11ProbeReq))


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--port', '-P', action='store', type=int, default=5555)
    parser.add_argument('--log-file', '-l', type=argparse.FileType('w+'))
    parser.add_argument('iface', action='store', help="the interface to monitor")
    parser.add_argument('miface', action='store', help="the monitor interface")
    args = parser.parse_args()
    # Publish results to socket
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % args.port)
    # Configure log utility
    logging.basicConfig(format="%(asctime)-15s\t%(levelname)-5s\t%(message)s",
        level=logging.INFO if not args.verbose else logging.DEBUG)
    # Start monitoring
    monitor(args.iface, args.miface, socket, logging.getLogger(__name__))


if __name__ == "__main__":
    run()

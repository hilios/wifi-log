"""A command line interface to monitor 802.11 network probe requests.
Usage:
    $ wifi-apc wlan0mon

For more info type:
    $ wifi-apc -h
"""
import argparse
import logging
import logging.handlers
import json
import os
import signal
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

    # Open socket
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    def handler(pkt):
        "Parses each package captured and publishes to log and socket."
        if pkt.haslayer(Dot11) :
            info = {'mac_address': pkt.addr2.upper(), 'ssid': pkt.info}
            logging.info("Found MAC: %(mac_address)s and SSID: %(ssid)s" % info)
            socket.send(json.dumps(info))

    logging.info("Monitoring network `%s` publishing at *:%s" % (iface, port))

    sniff(iface=iface, prn=handler, store=False,
        lfilter=lambda p: p.haslayer(Dot11ProbeReq))


def signal_handler(signal_code, frame):
    "Handle interrupt signals from the OS"
    logging.info("Bye, bye.")
    logging.shutdown()
    sys.exit(0)


def run():
    "Parses the CLI and run the application"
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--port', '-P', action='store', type=int, default=5555)
    parser.add_argument('--log-file', '-l', action='store',
        default='/var/log/wifi-apc/monitor.log')
    parser.add_argument('iface', action='store', help="the interface to monitor")
    args = parser.parse_args()
    # Log formatters
    defaultfmt = '%(asctime)s\t%(levelname)-8s\t%(message)s'
    consolefmt = '%(asctime)s %(filename)-15s %(levelname)-8s %(message)s'
    # Configure log utility
    logging.basicConfig(level=logging.INFO, format=defaultfmt)
    # Log to console debug messages
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(consolefmt))
    # Rotating file log
    logfile = logging.handlers.TimedRotatingFileHandler(args.log_file,
        when='midnight', utc=True)
    logfile.setLevel(logging.INFO)
    logfile.setFormatter(logging.Formatter(defaultfmt))
    logging.getLogger('').addHandler(logfile)
    # Setup signal handling to log bye messages
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    # Start monitoring
    monitor(args.iface, args.port)


if __name__ == "__main__":
    run()

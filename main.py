"""A command line interface to monitor 802.11 network probe requests.
Usage:
    $ wifi-apc wlan0mon

For more info type:
    $ wifi-apc -h
"""
import argparse
import datetime
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
        logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
        from scapy.all import sniff, Dot11ProbeReq, Dot11ProbeResp, Dot11
    except ImportError:
        print >> sys.stderr, "Did you install all the packager requirements?"
        sys.exit(1)

    logging.debug("Opening connection socket at *:%s" % port)
    # Open socket
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    def handler(pkt):
        "Parses each package captured and publishes to log and socket."
        if pkt.haslayer(Dot11) :
            rssi = (256 - ord(pkt.notdecoded[-2:-1])) * -1
            info = {'mac_address': pkt.addr2.upper(), 'ssid': pkt.info, 'rssi': rssi,}
            logging.info("{mac_address}\t{ssid}\t{rssi}".format(**info))
            socket.send(json.dumps(info))

    logging.debug("Monitoring interface `%s`" % iface)
    sniff(iface=iface, prn=handler, store=False,
        lfilter=lambda p: p.haslayer(Dot11ProbeReq))


def signal_handler(signal_code, frame):
    "Handle interrupt signals from the OS"
    logging.debug("Bye, bye.")
    logging.shutdown()
    sys.exit(0)


def run():
    "Parses the CLI and run the application"
    current_date = datetime.datetime.utcnow().strftime('%H-%M-%d.log')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--port', '-P', action='store', type=int, default=5555)
    parser.add_argument('--log-file', '-l', action='store',
        default='/var/log/wifi-apc.%s.log' % current_date)
    parser.add_argument('iface', action='store', help="the interface to monitor")
    args = parser.parse_args()
    # Create log dir
    log_dir = os.path.dirname(args.log_file)
    if not os.path.exists(log_dir):
        os.path.mkdir(log_dir)
    # Log formatters
    DEFAULT_FMT = '%(asctime)s\t%(levelname)-8s\t%(message)s'
    # Configure log utility
    logging.basicConfig(level=logging.DEBUG, format=DEFAULT_FMT)
    # Rotating file log
    
    logfile = logging.handlers.FileHandler(args.log_file)
    logfile.setLevel(logging.INFO)
    logfile.setFormatter(logging.Formatter(DEFAULT_FMT))
    logging.getLogger('').addHandler(logfile)
    # Setup signal handling to log bye messages
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    # Start WiFi scan
    logging.debug("Starting to sniff wifi signal")
    monitor(args.iface, args.port)


if __name__ == "__main__":
    run()

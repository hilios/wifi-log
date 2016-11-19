import logging
import os
import sys

log = logging.getLogger('sniffer')

if os.geteuid() != 0:
    print >> sys.stderr, "You need root permissions to run this program."
    sys.exit(1)

try:
    from scapy.all import sniff, Dot11Beacon, Dot11ProbeResp
except ImportError:
    log.error("Your system does not support sniffing")
    sys.exit(1)


def start(interface):
    "Start monitoring the given interface for probe requests."
    def pkt_handler(pkt):
        mac_address = pkt.addr2
        log.info(mac_address)

    sniff(iface=interface, prn=pkt_handler, store=False,
        lfilter=lambda p: (Dot11Beacon in p or Dot11ProbeResp in p))

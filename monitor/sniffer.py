import logging
import sys


log = logging.getLogger('sniffer')


try:
    from scapy.all import *
except ImportError:
    log.error("Your system does not support sniffing")
    sys.exit(1)


def process_pkt(pkt):
    bssid = pkt[Dot11].addr3
    log.info("")


def start():
    sniff(iface=interface, prn=process_pkt, store=False,
        lfilter=lambda p: (Dot11Beacon in p or Dot11ProbeResp in p))

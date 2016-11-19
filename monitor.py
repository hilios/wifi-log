import logging

log = logging.getLogger('sniffer')

if os.geteuid() != 0:
    print >> sys.stderr, "You need root permissions to run this program."
    sys.exit(1)

try:
    from scapy.all import sh
except ImportError:
    log.error("Your system does not support sniffing")
    sys.exit(1)


def start(interface):
    

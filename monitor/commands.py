import daemon
import lockfile
import logging
import os
import signal
import sys
import time
from datetime import date


log = logging.getLogger('cmd')

if os.geteuid() != 0:
    print >> sys.stderr, "You need root permissions to run this program."
    sys.exit(1)

try:
    # Setup the log dir
    os.makedirs('/var/log/apc')
except OSError as err:
    if not err.strerror in ['File exists']:
        raise err

PID_FILE = lockfile.FileLock('/var/run/apc.pid')
LOG_FILE = open('/var/log/apc/%s.log' % date.today().isoformat(), 'w+')


def start(interface, detached=False, log_file=None, url=None):
    if PID_FILE.is_locked():
        log.warn("Already running in, stop it before try again.")
        sys.exit(1)

    log.info('Starting to monitor')

    context = daemon.DaemonContext(detach_process=detached, umask=0o002,
        stdout=LOG_FILE if detached else log_file or sys.stdout,
        stderr=LOG_FILE if detached else log_file or sys.stderr,
        pidfile=PID_FILE,
    )
    context.signal_map = {
        # signal.SIGUSR1: reload_program_config,
        signal.SIGHUP:      'terminate',
        signal.SIGTERM :    'terminate',
    }
    context.files_preserve = [log_file, LOG_FILE]
    with context:
        try:
            from monitor import sniffer
            sniffer.start()
        except KeyboardInterrupt:
            log.info('Stopping, user interrupt')


def stop():
    if not PID_FILE.is_locked():
        log.warn("Nothing is running, did you started?")
        sys.exit(0)
    else:
        log.info('Stopping, terminate signal received')
        os.kill(PID_FILE.pid, signal.SIGTERM)


def install():
    log.info('Installing...')

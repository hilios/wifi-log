import daemon
import lockfile
import os
import signal
import sys
import time
from datetime import date

# Prepare the environment
try:
    os.makedirs('/var/lib/apc/log')

except OSError as err:
    if not err.strerror in ['File exists']:
        print(dir(err))
        sys.exit(1)


PID_FILE = lockfile.FileLock('/var/run/apc.pid')
LOG_FILE = open('/var/lib/apc/log/%s.log' % date.today().isoformat(), 'w+')


def start(detached):
    print('Starting...')
    context = daemon.DaemonContext(detach_process=detached, umask=0o002,
        working_directory='/var/lib/apc',
        stdout=LOG_FILE if detached else sys.stdout,
        stderr=LOG_FILE if detached else sys.stderr,
        pidfile=PID_FILE)
    context.signal_map = {
        # signal.SIGUSR1: reload_program_config,
        signal.SIGHUP:      'terminate',
        signal.SIGTERM :    'terminate',
    }
    context.files_preserve = [LOG_FILE]
    with context:
        while True:
            print("Hello, world!")
            time.sleep(5)


def stop(**kwargs):
    print("Bye, bye!")
    print(PID_FILE.pid)

    os.kill(PID_FILE.pid, signal.SIGTERM)

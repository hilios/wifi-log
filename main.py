import monitor.commands as cmd
import argparse
import logging


parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true')

subcmd = parser.add_subparsers()

start = subcmd.add_parser('start')
start.set_defaults(func=cmd.start)
start.add_argument('--url', '-u', action='store', default=None)
start.add_argument('--detached', '-d', action='store_true')
start.add_argument('--log-file', '-l', type=argparse.FileType('w+'))
start.add_argument('interface', action='store', help="the interface to monitor")

stop = subcmd.add_parser('stop')
stop.set_defaults(func=cmd.stop)


def run():
    args = parser.parse_args()
    kwargs = vars(args)

    verbose = kwargs.pop('verbose')
    logging.basicConfig(
        format="%(asctime)-15s\t%(levelname)-5s\t%(message)s",
        level=logging.INFO if not verbose else logging.DEBUG,
    )

    func = kwargs.pop('func')
    func(**kwargs)


if __name__ == '__main__':
    run()

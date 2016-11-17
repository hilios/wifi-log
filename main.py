import commands as cmd
import daemon
import argparse
import sys


parser = argparse.ArgumentParser()
subcmd = parser.add_subparsers()

start = subcmd.add_parser('start')
start.set_defaults(func=cmd.start)
start.add_argument('--detached', '-d', action='store_true')

stop = subcmd.add_parser('stop')
stop.set_defaults(func=cmd.stop)


def run():
    args = parser.parse_args()
    kwargs = vars(args)

    func = kwargs.pop('func')
    func(**kwargs)


if __name__ == '__main__':
    run()

import argparse
import logging


def run():
    "Parse the command line and run the application"
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--port', '-P', action='store', default=None)
    parser.add_argument('--log-file', '-l', type=argparse.FileType('w+'))

    parser.add_argument('interface', action='store', help="the interface to monitor")
    # Parse
    args = parser.parse_args()
    # Setup the logging
    logging.basicConfig(
        format="%(asctime)-15s\t%(levelname)-5s\t%(message)s",
        level=logging.INFO if not args.verbose else logging.DEBUG)
    # Execute the command
    monitor.start(args.interface)


if __name__ == '__main__':
    run()

#!/usr/bin/env python3
import argparse
import time
# local modules
from ebates_tracker import *


def parsearg():
    """parse arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('runcount',
            type=int,
            help="total times to run")
    parser.add_argument('-i','--interval',
            type=float,
            default=1.0,
            help="interval between two run, unit: hour, default: 1.0")
    return parser.parse_args()

def main():
    tracker = EbatesTracker()
    args = parsearg()
    # check args
    if args.runcount <= 0 or args.interval <= 0:
        raise ParseError('runcount and interval must be positive')
    # loop for args.runcount times
    for i in range(args.runcount):
        tracker.process(save_history=True)
        if i < args.runcount - 1:
            time.sleep(args.interval * 3600)


if __name__ == '__main__':
    main()

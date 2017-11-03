#!/usr/bin/env python3

import os
from ebates_tracker import *


def main():
    tracker = EbatesTracker()
    tracker.process(save_history=True)


if __name__ == '__main__':
    main()

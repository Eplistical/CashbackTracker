#!/usr/bin/env python3

from ebates_tracker import *
from cashback_tracker import CashbackTrackerDBMgr

def show_db():
    dbmgr = CashbackTrackerDBMgr()
    for a in dbmgr.get_history2():
        print(a)
    '''
    tracker = EbatesTracker()
    for key, data in tracker.get_history().items():
        print(key, ":")
        print()
        for updatetime, cashback in data:
            print(updatetime, cashback)
        print('-'*64)
    '''


if __name__ == '__main__':
    show_db()

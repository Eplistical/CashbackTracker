#!/usr/bin/env python3

from trackers.cashback_tracker import CashbackTrackerDBMgr

def show_db():
    dbmgr = CashbackTrackerDBMgr()
    for record in dbmgr.show():
        for tmp in record:
            print('%30s' % tmp, end=' ')
        print()


if __name__ == '__main__':
    show_db()

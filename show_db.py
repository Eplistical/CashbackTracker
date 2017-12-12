#!/usr/bin/env python3

from ebates_tracker import *
from cashback_tracker import CashbackTrackerDBMgr

def show_db():
    dbmgr = CashbackTrackerDBMgr()
    for record in dbmgr.show(name="Macy's", source="Ebates"):
        for tmp in record:
            print('%30s' % tmp, end=' ')
        print()


if __name__ == '__main__':
    show_db()

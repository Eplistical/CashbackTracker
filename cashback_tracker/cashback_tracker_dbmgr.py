# system modules
import sqlite3

# local modules
from .cashback_tracker_storeinfo import *


class CashbackTrackerDBMgr(object):
    """database manager for CashbackTracker
    """
    conn = None
    connected = False
    cursor = None

    def __init__(self, dbname='.CashbackTracker.db'):
        """init database
        """
        self.conn = sqlite3.connect(dbname)
        self.connected = True
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stores
                              ( name        VARCHAR,
                                source      VARCHAR,
                                cashback    VARCHAR,
                                updatetime  VARCHAR
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stores_history
                              ( name        VARCHAR,
                                source      VARCHAR,
                                cashback    VARCHAR,
                                updatetime  VARCHAR
                                )''')

    def __del__(self):
        """delete the object
        """
        if self.connected:
            self.conn.commit()
            self.conn.close()
            self.connected = False

    def __repr__(self):
        """print out database
        """
        rst = ""
        self.cursor.execute('''
                    SELECT name FROM sqlite_master
                    WHERE type='table'
                    ''')
        tables = self.cursor.fetchall()
        for table in tables:
            rst += '''
            TABLE: %s
            ''' % (table)
            self.cursor.execute('''
                    SELECT * FROM %s
                    ''' % table)
            rows = self.cursor.fetchall()
            for row in rows:
                rst += '''
                %20s%20s%40s
                ''' % row
        return rst

    def __contains__(self, obj):
        """check if a store exists
        """
        return (self.find(obj) is not None)

    def find(self, obj):
        """find info and return StoreInfo object
        """
        name = obj.name.replace("'", "''")
        source = obj.source.replace("'", "''")
        self.cursor.execute(
            '''SELECT * FROM stores
            WHERE name = '%s', source = '%s'
            ''' % (name, source))
        rows = self.cursor.fetchall()
        if len(rows) == 1:
            return StoreInfo(*rows[0])
        elif len(rows) == 0:
            return None
        else:
            raise CashBackTrackerError(
                'Find more than one record in database for ' + name)

    def delete(self, obj):
        """delete a piece of info in database,
            as well as all historical data
        """
        name = obj.name.replace("'", "''")
        source = obj.source.replace("'", "''")
        self.cursor.execute(
            '''DELETE FROM stores
            WHERE name = '%s', source = '%s'
            ''' % (name, source))
        self.cursor.execute(
            '''DELETE FROM stores_history
            WHERE name = '%s', source = '%s'
            ''' % (name, source))

    def update(self, obj):
        """update a piece of info
        """
        if obj not in self:
            self.cursor.execute(
                '''INSERT INTO stores
                VALUES ('%s', '%s', '%s' '%s')
                ''' % (obj.name.replace("'", "''"),
                       obj.source.replace("'", "''"),
                       obj.cashback,
                       obj.updatetime,
                       )
            )
        else:
            self.cursor.execute(
                '''UPDATE stores
                SET cashback = '%s', updatetime = '%s'
                WHERE name = '%s', source = '%s'
                '''% (obj.cashback,
                      obj.updatetime,
                      obj.name.replace("'", "''"),
                      obj.source.replace("'", "''"),
                      )
            )

    def record(self, obj):
        """record a piece of info as history cash back
        """
        self.cursor.execute(
            '''INSERT INTO stores_history
            VALUES ('%s', '%s', '%s', '%s')
            ''' % (obj.name.replace("'", "''"),
                   obj.source.replace("'", "''"),
                   obj.cashback,
                   obj.updatetime,
                   )
        )

    def get_history(self, obj):
        """get history data for a given store
        """
        name = obj.name.replace("'", "''")
        source = obj.source.replace("'", "''"),
        self.cursor.execute(
                '''SELECT cashback, updatetime FROM stores_history
                WHERE name = '%s', source = '%s'
                ''' % (name, source)
                )
        rows = self.cursor.fetchall()
        return rows


if __name__ == '__main__':
    print('This file contains database manager class for CashbackTracker')


# END

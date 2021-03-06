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
        return self.find(obj, None)

    def find(self, obj, txt_to_cashback_func=None):
        """find info and return StoreInfo object
        """
        name = obj.name.replace("'", "''")
        source = obj.source.replace("'", "''")
        self.cursor.execute(
            '''SELECT * FROM stores
            WHERE name = '%s' AND source = '%s'
            ''' % (name, source))
        rows = self.cursor.fetchall()
        if txt_to_cashback_func is None:
            # no cashback converter, only return found or not
            return len(rows) > 0
        else:
            # cashback converter passed, return StoreInfo object
            if len(rows) == 1:
                name, source, cashback_txt, updatetime = rows[0]
                cashback = txt_to_cashback_func(cashback_txt)
                return StoreInfo(name, source, cashback, updatetime)
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
            WHERE name = '%s' AND source = '%s'
            ''' % (name, source))
        self.cursor.execute(
            '''DELETE FROM stores_history
            WHERE name = '%s' AND source = '%s'
            ''' % (name, source))

    def update(self, obj):
        """update a piece of info
        """
        if obj not in self:
            self.cursor.execute(
                '''INSERT INTO stores
                VALUES ('%s', '%s', '%s', '%s')
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
                WHERE name = '%s' AND source = '%s'
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

    def show(self, name=None, source=None):
        """show records for given name and/or store
        """
        cmd = '''SELECT * FROM stores_history '''
        if name is None and source is not None:
            cmd += "WHERE source = '%s'" % source.replace("'", "''")
        elif name is not None and source is None:
            cmd += "WHERE name = '%s'" % name.replace("'", "''")
        elif name is not None and source is not None:
            cmd += "WHERE name = '%s' AND source = '%s'" % (
                    name.replace("'", "''"),
                    source.replace("'", "''"),
                    )
        self.cursor.execute(cmd)
        rows = self.cursor.fetchall()
        return rows
        



if __name__ == '__main__':
    print('This file contains database manager class for CashbackTracker')


# END

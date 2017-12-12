# system modules
import requests
from datetime import datetime
import warnings

# local modules
from .cashback_tracker_exceptions import *
from .cashback_tracker_storeinfo import *
from .cashback_tracker_cashback import *
from .cashback_tracker_dbmgr import *
from .cashback_tracker_alert import *


class CashbackTracker(object):
    """Base class for cashback tracker class
    """
    time_stamp_pattern = "%Y-%m-%d %H:%M:%S"
    source = None

    def __init__(self):
        """init object
        """
        self.dbmgr = CashbackTrackerDBMgr()
        self.query_store_list = self.load_query_store_list()
        self.store_list = None

    def process(self, save_history=False):
        """process stores in query_store_list

            Args
                @save_history: if True, save all history record
        """
        alert_list = list()
        alert_list_last = list()
        self.store_list = self.retrieve(self.query_store_list)

        for query_store, store in zip(self.query_store_list, self.store_list):
            # find the record in database
            last_store = self.dbmgr.find(store)
            # focus on new piece of data or cashback adjustment
            if last_store is None or store.cashback != last_store.cashback:
                self.dbmgr.update(store)
                if store.cashback >= query_store.alert_threash:
                    alert_list.append(store)
                    alert_list_last.append(last_store)
            # save history
            if save_history:
                self.dbmgr.record(store)
        # alert the changes
        if alert_list:
            CashbackTracker_alert(alert_list, alert_list_last)

    def load_query_store_list(self):
        """load query store list from QUERY_STORE_LIST file

            Returns
                #query_store_list: a list of QueryStoreInfo objects
        """
        with open('QUERY_STORE_LIST', 'r') as f:
            lines = f.read().split('\n')

        query_store_list = list()
        for line in lines:
            if line and not line.startswith('#'):
                s = line.split()
                name = " ".join(s[:-1]).strip()
                alert_threash = s[-1]
                query_store_list.append(
                        QueryStoreInfo(name, self.source, alert_threash)
                        )
        return query_store_list

    def retrieve(self, query_store_list=None):
        """retrieve information for query stores on Cashback
            if query_store_list is None, then retrieve all stores

            Args
                @query_store_list: a list of QueryStoreInfo objects

            Returns
                #rst: a list of StoreInfo objects corresponding to query_store_list
        """
        # dig info from text and convert to a list of StoreInfo objects
        all_store_list = self.retrieve_all_store_list()

        if query_store_list is None:
            rst = all_store_list
        else:
            all_store_name_list = [store.name for store in all_store_list]
            query_store_name_list = [store.name for store in query_store_list]
            rst = list()
            # the rst list must be aligned with query list
            for store_name in query_store_name_list:
                try:
                    idx = all_store_name_list.index(store_name)
                    rst.append(all_store_list[idx])
                except ValueError:
                    warnings.warn(
                    ''' No such a store named %s on Cashback, maybe an incorrect name.''' % store_name)
        return rst

    def retrieve_all_store_list(self):
        """make request and retrieve a list of StoreInfo
            this method should be overrided in children class

            Returns
               #all_store_list: a list of StoreInfo objects containing all stores for the cashback website
        """
        all_store_list = list()
        return all_store_list

    @staticmethod
    def make_request(url):
        """make request to retrieve website content from given url
            this is a helper method, should be used in retrieve_all_store_list()

            Args
                @url: website to retrieve

            Returns
                #r.text: website content
        """
        headers = {
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding' : 'gzip, deflate, br',
            'accept-language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        # retrieve data from web
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            raise RequestError("Error when retrieving info, status_code: %d " % r.status_code)


if __name__ == '__main__':
    print('This file contains core implimentation of CashbackTracker')


# END

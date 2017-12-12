from datetime import datetime
from bs4 import BeautifulSoup

from cashback_tracker import *


class EbatesTracker(CashbackTracker):
    """class for Ebates Tracker
    """
    source = 'Ebates'

    def retrieve_all_store_list(self):
        """make request and retrieve a list of StoreInfo
        """
        request_url = 'https://www.ebates.com/ajax/stores/sort.htm?sort=alpha'
        text = EbatesTracker.make_request(request_url)
        soup = BeautifulSoup(text, 'html.parser')
        updatetime = datetime.now().strftime(self.time_stamp_pattern)
        all_store_list = list()
        for divtag in soup.find_all('div'):
            name = divtag.find('a', {'class' : 'name-link'}).next.strip()
            cashback = divtag.find('a', {'class' : 'cb prox-r nohover rebate-link'}).next.strip()
            all_store_list.append(StoreInfo(name, self.source, cashback, updatetime))
        return all_store_list


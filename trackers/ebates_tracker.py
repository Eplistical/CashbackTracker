from datetime import datetime
import re
from bs4 import BeautifulSoup

from .cashback_tracker import CashbackTracker
from .cashback_tracker import CashBack
from .cashback_tracker import StoreInfo


class EbatesTracker(CashbackTracker):
    """class for Ebates Tracker
    """
    source = 'Ebates'

    def retrieve_all_store_list(self):
        """make request and retrieve a list of StoreInfo
        """
        # retrieve html
        request_url = 'https://www.ebates.com/ajax/stores/sort.htm?sort=alpha'
        text = self.make_request(request_url)
        # parse and extract all_store_list
        soup = BeautifulSoup(text, 'html.parser')
        updatetime = datetime.now().strftime(self.time_stamp_pattern)
        all_store_list = list()
        for divtag in soup.find_all('div'):
            name = divtag.find('a', {'class' : 'name-link'}).next.strip()
            cashback_txt = divtag.find('a', {'class' : 'cb prox-r nohover rebate-link'}).next.strip()
            cashback = self.txt_to_cashback(cashback_txt)
            all_store_list.append(StoreInfo(name, self.source, cashback, updatetime))
        return all_store_list

    def txt_to_cashback(self, txt):
        """Convert string to CashBack object.

            Args
                @txt: a string describing cashback

            Returns
                #rst: a CashBack object

            Ebates possible txt format:
                2.0%
                2.0% Cash Back
                Up to 2.0%
                Up to 2.0% Cash Back
                $2.00
                $2.00 Cash Back
                Up to $2.00
                Up to $2.00 Cash Back
                No Discount
                Coupons Only
                In-Store Cash Back only
        """
        cashback_pattern = re.compile('(Up to )?(\$)?([\.\d]*)(%)?( Cash Back)?')
        if txt in ( 'No Discount',
                    'Coupons Only',
                    'In-Store Cash Back only'):
            value = 0.0
            measure = CashBack.BY_PERCENT
            up_to = False
        else:
            info = cashback_pattern.search(txt)
            up_to = (info.group(1) is not None)
            value = float(info.group(3))
            if info.group(2) is not None:
                measure = CashBack.BY_DOLLAR
            elif info.group(4) is not None:
                measure = CashBack.BY_PERCENT
            else:
                raise ValueError('Incompatible Cashback Format')
        return CashBack(value, measure, up_to)


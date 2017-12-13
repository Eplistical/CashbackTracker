from datetime import datetime
import re
from bs4 import BeautifulSoup

from .cashback_tracker import CashbackTracker
from .cashback_tracker import CashBack
from .cashback_tracker import StoreInfo


class CouponCactusTracker(CashbackTracker):
    """class for CouponCactus Tracker
    """
    source = 'CouponCactus'

    def retrieve_all_store_list(self):
        """make request and retrieve a list of StoreInfo
        """
        updatetime = datetime.now().strftime(self.time_stamp_pattern)
        all_store_list = list()
        # retrieve html
        request_url = 'https://www.couponcactus.com/coupons'
        text = self.make_request(request_url)
        # parse and extract all_store_list
        soup = BeautifulSoup(text, 'html.parser')
        for row in soup.find_all('tr', {'class' : ' body-content'}):
            cell = row.find_all('td')
            name = cell[0].find('a').next.strip()
            if name.endswith(' coupons'):
                name = name[:-8]
            cashback_txt = cell[1].next.strip()
            cashback = self.txt_to_cashback(cashback_txt)
            all_store_list.append(StoreInfo(name, self.source, cashback, updatetime))
        return all_store_list

    def txt_to_cashback(self, txt):
        """Convert string to CashBack object, for CouponCactus

            Args
                @txt: a string describing cashback

            Returns
                #rst: a CashBack object

            CouponCactus possible txt format:
                2.0%
                $2.00
        """
        cashback_pattern = re.compile('(\$)?([\.\d]*)(%)?')
        info = cashback_pattern.search(txt)
        up_to = False
        value = float(info.group(2))
        if info.group(1) is not None:
            measure = CashBack.BY_DOLLAR
        elif info.group(3) is not None:
            measure = CashBack.BY_PERCENT
        else:
            raise ValueError('Incompatible Cashback Format')
        return CashBack(value, measure, up_to)


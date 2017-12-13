from datetime import datetime
import string
import re
from bs4 import BeautifulSoup

from .cashback_tracker import CashbackTracker
from .cashback_tracker import CashBack
from .cashback_tracker import StoreInfo


class BeFrugalTracker(CashbackTracker):
    """class for BeFrugal Tracker
    """
    source = 'BeFrugal'

    def retrieve_all_store_list(self):
        """make request and retrieve a list of StoreInfo
        """
        updatetime = datetime.now().strftime(self.time_stamp_pattern)
        all_store_list = list()
        # loop over labels = ['a', 'b', ..., 'z', 'num']
        labels = list(string.ascii_lowercase)
        labels.append('num')
        for label in labels:
            # retrieve html
            request_url = 'https://www.befrugal.com/coupons/stores/%s/' % label
            text = self.make_request(request_url)
            # parse and extract all_store_list
            soup = BeautifulSoup(text, 'html.parser')
            allstore_table = soup.find('div', {'class' : 'table-responsive allstores-table'})
            for i, item in enumerate(allstore_table.find_all('tr')):
                if i == 0: 
                    continue
                cell = item.find_all('td')
                name = cell[0].find('a').next.strip()
                cashback_txt = cell[1].next.strip()
                cashback = self.txt_to_cashback(cashback_txt)
                all_store_list.append(StoreInfo(name, self.source, cashback, updatetime))
        return all_store_list

    def txt_to_cashback(self, txt):
        """Convert string to CashBack object, for BeFrugal

            Args
                @txt: a string describing cashback

            Returns
                #rst: a CashBack object

            Ebates possible txt format:
                "" (empty)
                2.0%
                Up to 2.0%
                $2.00
                Up to $2.00
        """
        cashback_pattern = re.compile('(Up to )?(\$)?([\.\d]*)(%)?')
        if txt == '':
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

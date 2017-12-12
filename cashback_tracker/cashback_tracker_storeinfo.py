from .cashback_tracker_cashback import *

class QueryStoreInfo(object):
    """A class storing query information for a store
    """
    def __init__(self, name, source, alert_threash):
        """init
        """
        self.name = name
        self.source = source
        if isinstance(alert_threash, CashBack):
            self.alert_threash = alert_threash
        else:
            self.alert_threash = CashBack(alert_threash)

    def __repr__(self):
        """print out
        """
        rst = """
        name: %s
        source: %s
        alert threash: %s
        """ % (self.name, self.source, self.alert_threash)
        return rst


class StoreInfo(object):
    """A class storing information for a given store
    """
    def __init__(self, name, source, cashback, updatetime):
        """init
        """
        self.name = name
        self.source = source
        if isinstance(cashback, CashBack):
            self.cashback = cashback
        else:
            self.cashback = CashBack(cashback)
        self.updatetime = updatetime

    def __repr__(self):
        """print out
        """
        rst = """
        name: %s
        source: %s
        cashback: %s
        updatetime: %s
        """ % (
                self.name,
                self.source,
                self.cashback,
                self.updatetime)
        return rst


if __name__ == '__main__':
    print('This file contains implimentation for StoreInfo')


# END

from .cashback_tracker_cashback import *

class QueryStoreInfo(object):
    """A class storing query information for a store
    """
    def __init__(self, name, source, alert_threash):
        """init
        """
        assert isinstance(alert_threash, CashBack)
        self.name = name
        self.source = source
        self.alert_threash = alert_threash

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
        assert isinstance(cashback, CashBack)
        self.name = name
        self.source = source
        self.cashback = cashback
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

import re

class CashBack(object):
    """A class storing cashback info
    """
    BY_PERCENT = 1
    BY_DOLLAR = -1

    CASHBACK_PATTERN = re.compile('(Up to )?(\$)?([\.\d]*)(%)?( Cash Back)?')

    def __init__(self, txt):
        """init from a txt retrieved from Ebates

            Possible format:
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
        if txt in ( 'No Discount', 
                    'Coupons Only', 
                    'In-Store Cash Back only'):
            self.value = 0.0
            self.measure = self.BY_PERCENT
            self.up_to = False
        else:
            cashback = self.CASHBACK_PATTERN.search(txt)
            self.up_to = (cashback.group(1) is not None)
            self.value = float(cashback.group(3))
            if cashback.group(2) is not None:
                self.measure = self.BY_DOLLAR
            elif cashback.group(4) is not None:
                self.measure = self.BY_PERCENT
            else:
                raise ValueError('Incompatible Cashback Format')

    def __repr__(self):
        """print out
        """
        rst = "Up to " if self.up_to else ""
        if self.measure == self.BY_DOLLAR:
            rst += "$%.2f" % self.value
        else:
            rst += "%.1f" % self.value + '%'
        return rst

    def __lt__(self, other):
        """operator: <
        """
        return (self.measure == other.measure
                and self.value < other.value)

    def __le__(self, other):
        """operator: <=
        """
        return (self.measure == other.measure
                and self.value <= other.value)

    def __gt__(self, other):
        """operator: >
        """
        return (self.measure == other.measure
                and self.value > other.value)

    def __ge__(self, other):
        """operator: >=
        """
        return (self.measure == other.measure
                and self.value >= other.value)

    def __eq__(self, other):
        """operator: ==
        """
        return (self.measure == other.measure
                and self.value == other.value
                and self.up_to == other.up_to)

    def __neq__(self, other):
        """operator: !=
        """
        return not (self == other)

# END

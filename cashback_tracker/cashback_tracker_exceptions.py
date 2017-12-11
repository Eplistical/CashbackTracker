class CashbackTrackerError(Exception):
    """exception
    """


class RequestError(CashbackTrackerError):
    """raised when something wrong with web info request
    """


class ParseError(CashbackTrackerError):
    """raised when something wrong during parsing text
    """


class AlertError(CashbackTrackerError):
    """raised when something wrong during alerting users
    """



if __name__ == '__main__':
    print('This file contains exceptions used in CashbackTracker')

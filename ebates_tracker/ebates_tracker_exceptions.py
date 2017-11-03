class EbatesTrackerError(Exception):
    """exception
    """


class RequestError(EbatesTrackerError):
    """raised when something wrong with web info request
    """


class ParseError(EbatesTrackerError):
    """raised when something wrong during parsing text
    """


class AlertError(EbatesTrackerError):
    """raised when something wrong during alerting users
    """



if __name__ == '__main__':
    print('This file contains exceptions used in EbatesTracker')

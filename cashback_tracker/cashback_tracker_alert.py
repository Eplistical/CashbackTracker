# system modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# local modules
from .cashback_tracker_exceptions import *
from .cashback_tracker_storeinfo import *


__all__ = ['CashbackTracker_alert']


def generate_alert_txt(now_info_list, last_info_list):
    """generate alert text
    """
    rst = """
        ALERT: Cash back changes
        ---------------------------------------------------------------------------------------
        %20s%20s%20s%20s
        ---------------------------------------------------------------------------------------
    """[1:-1] % ('Name', 'Source', 'Now Cashback', 'Last Cashback')

    for now_info, last_info in zip(now_info_list, last_info_list):
        last_cashback = None if last_info is None else last_info.cashback
        rst += """
        %20s%20s%20s%20s
        """[:-1] % (now_info.name, now_info.source,
                now_info.cashback, last_cashback)
    rst += """
        ---------------------------------------------------------------------------------------
    """
    return rst


def alert_by_print(now_info_list, last_info_list):
    """alert by printing out, for debug
    """
    print(generate_alert_txt(now_info_list, last_info_list))


def alert_by_email(now_info_list, last_info_list):
    """alert by email
    """
    Subject = 'CashbackTracker Alert'
    From = 'reminder@CashbackTracker.com'
    # generate recipients
    To = ''
    with open('ALERT_ADDR', 'r') as f:
        ALERT_ADDR = f.read().split('\n')
    for line in ALERT_ADDR:
        if line and not line.startswith('#'):
            To += line + ','
    To = To[:-1]
    # if no recipient
    if To.strip() == '':
        raise AlertError('No recipient to alert, please setup ALERT_ADDR file first.')
    # generate msg object
    msg = MIMEMultipart()
    msg['From'] = From
    msg['To'] = To
    msg['Subject'] = Subject
    txt = generate_alert_txt(now_info_list, last_info_list)
    msg.attach(MIMEText(txt, 'plain'))
    # send email
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
    s.quit()


def CashbackTracker_alert(now_info_list, last_info_list):
    """alert cashback for given new & old StoreInfo objects
    """
    alert_by_print(now_info_list, last_info_list)
    #alert_by_email(now_info_list, last_info_list)


if __name__ == '__main__':
    print('''
    This file contains the alert function for CashbackTracker.
    One may modify this file to custimize how to notify the cashback changes.
    ''')

# END

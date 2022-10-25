from datetime import datetime
from pytz import timezone

def count_time(event_date):
    tz = timezone('EST')
    now_time = datetime.now(tz)
    time_delta = event_date.replace(tzinfo=None) - now_time.replace(tzinfo=None)
    days = time_delta.days
    seconds = time_delta.seconds
    if days == 356:
        string = "Trip in 1 year."
    elif days > 365:
        if days % 365 == 0:
            string = "Trip in {} years".format(days/365)
        else:
            string = "Trip in {} years, {} days.".format(days//365,days%365)
    elif days < 365:
        if days == 0:
            string = "Trip in {} hours.".format(seconds // (60*60))
        elif days > 0:
            string = "Trip in {} days.".format(days)
        else :
            string = "Trip has allready occured."
    return string
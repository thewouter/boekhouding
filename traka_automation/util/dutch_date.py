import locale
from datetime import date, datetime


def dutch_date(date_time: datetime | date):
    """format datetime in Dutch format."""

    locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")  # Dutch dates
    return date_time.strftime("%-d %B %Y")

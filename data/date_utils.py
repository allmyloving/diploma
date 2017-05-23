from datetime import date
from datetime import timedelta


def tomorrow():
    return today() + timedelta(days=1)


def today():
    return date.today()


def minus_days(date, days):
    return date - timedelta(days)

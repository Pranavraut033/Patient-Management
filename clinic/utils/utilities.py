import datetime
from django.utils import timezone
import re
from datetime import date

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper() + \
            mo.group(0)[1:].lower(), s)

def get_adv_date(days=7, years=0):
    return timezone.now() + datetime.timedelta(days=(days + 365.2504*years))

def formate(kwargs):
    return kwargs

def getAge(from_date):
    today = date.today()
    return today.year - from_date.year - ((today.month, today.day) < (from_date.month, from_date.day))

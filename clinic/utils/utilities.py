import datetime
from django.utils import timezone
import re

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper() + \
            mo.group(0)[1:].lower(), s)

def get_adv_date(days=7):
    return timezone.now() + datetime.timedelta(days=days)

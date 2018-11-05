from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

import re
from validate_email import validate_email as ve

import clinic.utils.re_pattern as rep
from clinic import models as m

error_codes = ['urname_ptrn_mismatch', 'urname_exists', 'pass_ptrn_mismatch',\
                'email_ptrn_mismatch', 'ur_404', 'pin_invalid', 'num_invalid', 'integer_only', ]

errors = {
    error_codes[0] : 'Given username "%(value)s" is invalid!',
    error_codes[1] : 'Doctor with username "%(value)s" exists!',
    error_codes[2] : "Password should have an upper-case, a lower-case and a numeric character",
    error_codes[3] : 'Given email-id "%(value)s" is invalid!',
    error_codes[4] : 'Username: "%(value)s" does not exists!',
    error_codes[5] : '"%(value)s" is invalid!',
    error_codes[6] : 'Phone number should be of ten digit',
    error_codes[7] : 'This Field requires integer value only given "%(value)s"',
    # 4 : 'Username "%s" disabled by Administrator',
}

def raise_err(code, value=None):
    raise ValidationError (
        _(errors[error_codes[code]]),
        code=error_codes[code],
        params={'value': value}, )

def validate_username_create(value):
    validate_username(value)
    try:
        m.Doctor.objects.get(pk=value)
        raise_err(1, value)
    except ObjectDoesNotExist:
        pass

def validate_username_login(value):
    validate_username(value)
    try:
        m.Doctor.objects.get(pk=value)
    except Exception as e:
        raise_err(4,value)

def validate_username(value):
    if not re.match(rep.username_pattern, value):
        raise_err(0, value)

def validate_password(value):
    if not re.match(rep.password_pattern, value):
        raise_err(2)

def validate_email(value):
    if not ve(value):
        raise_err(3, value)

def validate_pincode(value):
    value = re.sub(r'[\s-]', '', str(value))
    if not value.isnumeric():
        raise_err(7, value)
    elif not len(value) == 6:
        raise_err(5, value)

def validate_number(value):
    value = str(value)

    value = re.sub(r'[\s-]', '', value).replace('+91', '', 1)
    if value[0] == 0:
        value = value.replace('0', '', 1)

    if not value.isnumeric():
        raise_err(7, value)
    elif not len(value) == 10:
        raise_err(6)

username_pattern = r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$'

# Password (UpperCase, LowerCase and Number)
password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$'
# Password (UpperCase, LowerCase, Number/SpecialChar and min 8 Chars)
# password_pattern = r'(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'

from django import template

import re
from ..utils import log

logger = log.Logger()

register = template.Library()

@register.simple_tag(name='sub')
def sub(str1, length):
    post = ''
    if not isinstance(str1, str): str1 = str(str1)
    if len(str1) < length:
        return str1;
    if(len(str1) > length + 3):
        post = '...'
        length = length - 3
    return str1[:length] + post

@register.simple_tag(name='id')
def gen_id(str):
    return str.replace(' ', '_').lower();

@register.simple_tag(name='title')
def titlecase(s):
    s = s.replace('_', ' ')
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper() + \
            mo.group(0)[1:].lower(), s)

@register.simple_tag(name='err')
def get_error(errors, field):
    try:
        return errors[field]
    except Exception as e:
        return ''

@register.simple_tag(name='value')
def get_value(form, field):
    return form[field]

@register.simple_tag(name='log')
def logthis(*value):
    logger.web(*value)

# https://vinta.ws/code/how-to-set-a-variable-in-django-template.html
class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ''
        context[self.var_name] = value

        return u''

@register.tag(name='set')
def set_var(parser, token):
    '''
    {% set some_var = '123' %}
    '''
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])
######################################################################################

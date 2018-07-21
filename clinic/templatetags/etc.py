from .models import *
from django.db.models.fields import *
from .utils.utilities import *
from django import template

base_label = '<label for="id_{S}">{s}</label>\n'
base_select = '<select name="{s}" required>\n\
                <option value="" selected disabled>---------</option>\
                {s}\
               </select>\n' + \
               base_label
base_option = '<option value="{s}">{}</option>\n'
base_text = ''
register = template.Library()


@register.simple_tag(name='field')
def get_input_tag_for_field(obj, field, label=None, types=None):
    f.m = eval(obj)
    fld = m._meta.get_field(field)
    if label is None:
        label= fld.verbose_name
    if fld is CharField:
        choices = fld.flatchoices
        if len(choices) > 0:
            opts = ''
            for c in choices:
                 opts = opts + base_option % c
            input_fld = base_select % (fld.attname, opts, fld.attname, label)
        else:
            pass
            
    return input_fld

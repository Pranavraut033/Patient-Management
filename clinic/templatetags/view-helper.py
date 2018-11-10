from django.db.models.fields import *
from .utilities import titlecase, logthis
from django import template

register = template.Library()

def is_required(field):
    return not (field.null or field.blank)

def get_default(field):
    return None if field.default is NOT_PROVIDED else field.default

'''
    kwargs: icon, i_opts 'icon-options', options 'string for all other attribute'
'''
def input_generic(object, field_name, col='', label=None, **kwargs):
    field = object._meta.get_field(field_name)
    if label is None:
        label = titlecase(field.verbose_name)
    context = {'field' : field, 'label' : label, 'col' : col, \
            'required' : is_required(field), }
    try:
        dval = kwargs['extra']['values'][field_name]
        if not dval: context['default'] = dval
        else: raise Exception
    except Exception as e:
        if not 'value' in kwargs.keys():
            context['default'] = get_default(field)
    context = {**context , **kwargs}
    context['i_opts'] = 'prefix'
    return context;

@register.inclusion_tag('clinic/elements/text-input.html')
def input(object, field_name, col='', type='text', label=None, **kwargs):
    context = input_generic(object, field_name, col, label, **kwargs)
    context['type'] = type
    return context

@register.inclusion_tag('clinic/elements/select-input.html')
def select(object, field_name, col='', label=None, **kwargs):
    context = input_generic(object, field_name, col, label, **kwargs)
    context['vals'] = object._meta.get_field(field_name).flatchoices
    return context

@register.inclusion_tag('clinic/elements/textarea-input.html')
def textarea(object, field_name, length, col='', label=None, rows=2, **kwargs):
    context = input_generic(object, field_name, col=col,label=label, **kwargs);
    context['rows'], context['length'] = rows, length
    return context

@register.inclusion_tag('clinic/elements/file-input.html')
def file(object, field_name, col='', accept='*', label=None, **kwargs):
    context = input_generic(object, field_name, col=col,label=label, **kwargs);
    context['file_type'] = accept
    return context

# @register.inclusion_tag('clinic/elements/checkbox.html')
# def checkbox(object, field_name, col='', accept='*', label=None, **kwargs):
#     context = input_generic(object, field_name, col, label, **kwargs)
#     return context;

@register.inclusion_tag('clinic/elements/sidebar-item.html')
def sub_menu_e(title, **kwargs):
    # 'object' :
    context = {'title' : title, }
    context = {**context, **kwargs}
    return context

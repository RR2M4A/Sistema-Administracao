from django import template
import re


register = template.Library()


@register.filter
def format_cpf(value):
    '''
    Formats a cpf (numeric-only at the start) to 000.000.000-00
    '''

    value = re.sub(r'\D', '', str(value))

    if len(value) == 11:
        return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', value)

    return value


@register.filter
def format_phone_number(value):
    '''
    Formats a phone number to (00) 00000-0000 or (00) 0000-0000
    '''

    value = re.sub(r'\D', '', str(value))

    if len(value) == 11:
        return re.sub(r'(\d{2})(\d{5})(\d{4})', r'(\1) \2-\3', value)

    if len(value) == 10:
        return re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', value)

    return value
from django import template
from django.utils.safestring import mark_safe

import markdown2

register = template.Library()

@register.filter(name='markdown_to_html')
def markdown_to_html(markdown_text):
    '''Converts markdown text to HTML '''   
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)

@register.filter(name='cut_image')
def cut_image(url):
    '''Fixes image problem'''
    return url[6:]


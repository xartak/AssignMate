from django import template
from ..models import Homework
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag
def total_homeworks():
    return Homework.published.count()

@register.inclusion_tag('assign/homework/latest_homeworks.html')
def show_latest_homeworks(count=5):
    latest_homeworks = Homework.published.order_by('-publish')[:count]
    return {'latest_homeworks': latest_homeworks}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
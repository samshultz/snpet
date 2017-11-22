from django.db.models import Count
from django.contrib.auth.models import User
from django import template
register = template.Library()
from ..models import Snippet, Language

@register.inclusion_tag('snippets/latest_snippets.html')
def show_latest_snippets(count=5):
    latest_snippets = Snippet.objects.order_by('-created')[:count]
    return {'latest_snippets': latest_snippets}

@register.assignment_tag
def get_most_popular_languages(count=5):
    return Language.objects.annotate(
        total_users=Count('users')
        ).order_by('-total_users')[:count]

@register.assignment_tag
def get_top_authors(count=5):
    return User.objects.annotate(
        total_snippets=Count('snippets_created')
        ).order_by('-total_snippets')[:count]
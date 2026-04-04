from django import template

register = template.Library()

@register.simple_tag
def display_rank_or_role(user):
    if user.academic_rank == 'Student':
        return 'Role:'
    return 'Academic Rank:'
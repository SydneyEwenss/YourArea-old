from django import template
from YourArea.models import Notification

register = template.Library()

@register.inclusion_tag('YourArea/tags/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
    return {'notifications': notifications}

@register.inclusion_tag('YourArea/tags/show_posts.html', takes_context=True)
def show_posts(context, posts):
    request_user = context['request'].user
    return {'posts': posts, 'user': request_user}

@register.inclusion_tag('YourArea/tags/show_area_list_profile.html')
def show_area_list(profiles):
    print(profiles)
    return {'profiles': profiles}
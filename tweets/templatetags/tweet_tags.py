from django import template
from tweets.models import Tweet

register = template.Library()

@register.filter
def check_if_liked(user_id, tweet_id):
    try:
        tweet_data = Tweet.objects.get(id = tweet_id)
        return tweet_data.like.filter(id = user_id).exists()
    except Tweet.DoesNotExist:
        return 'Unknown'

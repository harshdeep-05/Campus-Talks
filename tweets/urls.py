from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.feed),
	url(r'^(?P<user_username>\w+)/(?P<tweet_id>\w+)/$', views.single_tweet),
	url(r'^post_tweet/$', views.add_tweet),
	url(r'^search', views.search, name='search'),
	url(r'^like', views.like),
	url(r'^retweet', views.retweet)
]

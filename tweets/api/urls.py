from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$', views.TweetListAPIView.as_view(), name='list'),
    url(r'^create/$', views.TweetCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.TweetDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.TweetUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.TweetDeleteAPIView.as_view(), name='delete'),
]

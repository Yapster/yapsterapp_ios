from django.conf.urls import patterns, include, url
from stream.views_api import *

urlpatterns = patterns('stream.views_api',
	url(r'^load/$',LoadStream.as_view()),
	url(r'^menu/load/$',LoadStreamMenu.as_view()),
	url(r'^trending/load/$',LoadTrendingStream.as_view()),
	url(r'^channel/load/$',LoadChannelStream.as_view()),
)

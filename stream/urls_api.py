from django.conf.urls import patterns, include, url
from stream.views_api import *

print LoadStream

urlpatterns = patterns('stream.views_api',
	url(r'^load/$',LoadStream.as_view()),
)

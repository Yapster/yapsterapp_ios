from django.conf.urls import patterns, include, url
from notification.views_api import *

urlpatterns = patterns('notification.views_api',
	url(r'^all/load/$',LoadAllNotifications.as_view()),
	url(r'^unread/load/$',LoadUnreadNotifications.as_view()),
	url(r'^read/$',NotificationsRead.as_view()),
	url(r'^clicked/$',NotificationsClicked.as_view()),
)
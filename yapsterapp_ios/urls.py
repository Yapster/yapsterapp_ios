from django.conf.urls import patterns, include, url
import yapsterapp_ios.views
from yap.views_api import yap

urlpatterns = patterns('',
	#url(r'^$',"yapsterapp_ios.views.index"),
	url(r'^$',"yapsterapp_ios.views.aws_index"),
	url(r'^api/0\.0\.1/',include(patterns('',
		url(r'users/',include('users.urls_api')),
		url(r'notification/',include('notification.urls_api')),
		url(r'stream/',include('stream.urls_api')),
		url(r'yap/',include('yap.urls_api')),
		url(r'location/',include('location.urls_api')),
		url(r'search/',include('search.urls_api')),
		url(r'report/',include('report.urls_api')),
		url(r'questionaire/',include('questionaire.urls_api')),
		#url(r'',include('urls_api')),
		))),
	url(r'^yap/',include(patterns('',
		url(r'^(?P<yap_id>[0-9]+)/$',yap, name='yap'),
		))),
	url(r'^reyap/',include(patterns('',
		url(r'^(?P<reyap_id>[0-9]+)/$',yap, name='reyap'),
		))),
)
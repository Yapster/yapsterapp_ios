from django.conf.urls import patterns, include, url
import yapsterapp_ios.views

urlpatterns = patterns('',
	url(r'^$',"yapsterapp_ios.views.index"),
	url(r'^api/0\.0\.1/',include(patterns('',
		url(r'users/',include('users.urls_api')),
		url(r'notification/',include('notification.urls_api')),
		url(r'stream/',include('stream.urls_api')),
		url(r'yap/',include('yap.urls_api')),
		url(r'location/',include('location.urls_api')),
		url(r'search/',include('search.urls_api')),
		url(r'report/',include('report.urls_api')),
		#url(r'',include('urls_api')),
	))),
)
from django.conf.urls import patterns, include, url
from report.views_api import *

urlpatterns = patterns('report.views_api',
	url(r'^yap/$',ReportYap.as_view()),
	url(r'^reyap/$',ReportReyap.as_view()),
	url(r'^user/$',ReportUser.as_view()),
	url(r'^bug/$',ReportBug.as_view()),
	url(r'^general/$',ReportGeneral.as_view()),
)
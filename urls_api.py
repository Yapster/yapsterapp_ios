from django.conf.urls import patterns, include, url
from 

urlpatterns = patterns('',
	url(r'^profile/info/$',ProfileInfo.as_view()),
	url(r'^profile/stream/$',ProfileStreams.as_view()),
	url(r'^profile/followers/$',ListOfFollowers.as_view()),
	url(r'^profile/following/$',ListOfFollowing.as_view()),
	url(r'^profile/editprofile/load/$',LoadProfile.as_view()),
	#url(r'^delete/$',UserDelete.as_view()),
	url(r'^sign_in/$',SignIn.as_view()),
	url(r'^recommended/$',Recommendations.as_view()),
	url(r'^sign_up/$',SignUp.as_view()),
	url(r'^settings/$',Settings.as_view()),
	url(r'^setsession/$','session_id'),
	url(r'^recommend/$',RecommendUser.as_view()),
	url(r'^unrecommend/$',UnrecommendUser.as_view()),
	url(r'^verify/$',VerifyUser.as_view()),
	url(r'^unverify/$',UnverifyUser.as_view()),

)
from django.conf.urls import patterns, include, url
from questionaire.views_api import *

urlpatterns = patterns('questionaire.views_api',
	url(r'^no_yaps_in_stream_questionaire/first_quesion/$',FirstQuestionOfNoYapsInStreamQuestionaire.as_view()),
	url(r'^no_yaps_in_stream_questionaire/next_question/$',NextQuestionOfNoYapsInStreamQuestionaire.as_view()),
	url(r'^no_yaps_in_stream_questionaire/answer/$',AnswerQuestionOfNoYapsInStreamQuestionaire.as_view()),

)
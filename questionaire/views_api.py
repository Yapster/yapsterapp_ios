from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from yapster_utils import check_session
from questionaire.serializers import *

class FirstQuestionOfNoYapsInStreamQuestionaire(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if Question.objects.filter(is_active=True).count() >= 1:
				question1 = Question.objects.filter(is_active=True)[0]
				serialized = QuestionSerializer(question1,data=self.request.DATA)
				return Response(serialized.data)
			else:
				return Response(None)
		else:
			return Response(check[0])

class NextQuestionOfNoYapsInStreamQuestionaire(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if "question_id" in kwargs:
				try:
					question = Question.objects.get(pk=kwargs.get("question_id"))
				except ObjectDoesNotExist:
					return Response(None)
				serialized = QuestionSerializer(question,data=self.request.DATA)
				return Response(serialized.data)
			else:
				return Response({"valid":False,"messsage":"For this request you must request using a question_id."})
		else:
			return Response(check[0])

class AnswerQuestionOfNoYapsInStreamQuestionaire(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.get('user_id'))
		check = check_session(user=user,session_id=kwargs.get('session_id'))
		if check[1]:
			question_answers = kwargs.get("question_answers")
			question = Question.objects.get(pk=kwargs.get("question_id"))
			if Answer.objects.filter(user=user,question=question,is_active=True).exists() == True:
				previous_answers_for_this_question_by_this_user = Answer.objects.filter(user=user,question=question,is_active=True)
				for previous_answer_for_this_question_by_this_user in previous_answers_for_this_question_by_this_user:
					previous_answer_for_this_question_by_this_user.is_active = False
					previous_answer_for_this_question_by_this_user.save(update_fields=['is_active'])
			for question_answer in question_answers:
				try:
					chosen_answer = QuestionPossibleAnswer.objects.get(pk=question_answer)
				except ObjectDoesNotExist:
					if Answer.objects.filter(user=user,question=question,is_active=False).exists == True:
						previous_answers_for_this_question_by_this_user = Answer.objects.filter(user=self.user,question=self.question,is_active=True)[:1]
						for previous_answer_for_this_question_by_this_user in previous_answers_for_this_question_by_this_user:
							previous_answer_for_this_question_by_this_user.is_active = True
							previous_answer_for_this_question_by_this_user.save(update_fields=["is_active"])
					return Response({"valid":False, "message":"Question answer given does not exist."})
				this_answers_possible_answers = question.question_possible_answers.filter(is_active=True)
				if chosen_answer in this_answers_possible_answers:
					created_answer = Answer.objects.create(user=user,question=question,chosen_answer=chosen_answer)
					if isinstance(created_answer,str):
						if Answer.objects.filter(user=user,question=question,is_active=False).exists == True and question.question_type.pk != 2:
							previous_answers_for_this_question_by_this_user = Answer.objects.filter(user=self.user,question=self.question,is_active=True)[:1]
							for previous_answer_for_this_question_by_this_user in previous_answers_for_this_question_by_this_user:
								previous_answer_for_this_question_by_this_user.is_active = True
								previous_answer_for_this_question_by_this_user.save(update_fields=["is_active"])
						return Response({"valid":False,"message":created_answer})
				else:
					if Answer.objects.filter(user=user,question=question,is_active=False).exists == True and question.question_type.pk != 2:
						previous_answers_for_this_question_by_this_user = Answer.objects.filter(user=self.user,question=self.question,is_active=True)[:1]
						for previous_answer_for_this_question_by_this_user in previous_answers_for_this_question_by_this_user:
							previous_answer_for_this_question_by_this_user.is_active = True
							previous_answer_for_this_question_by_this_user.save(update_fields=["is_active"])
					return Response({"valid":False, "message":"This answer is not a possible answer choice for this question."})
			return Response({"valid":True, "message":"Question answer successfuly recorded."})





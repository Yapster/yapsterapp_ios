from rest_framework import serializers
from django.contrib.auth.models import User
from questionaire.models import *

class QuestionTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = QuestionType
		fields = ("question_type_id","question_type_name")

class QuestionPossibleAnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = QuestionPossibleAnswer
		fields = ("question_possible_answer_id","question_possible_answer_text")

class QuestionSerializer(serializers.ModelSerializer):

	total_number_of_questionaire_questions = serializers.SerializerMethodField('get_total_number_of_questionaire_questions')
	list_of_questionaire_questions_ids = serializers.SerializerMethodField('get_list_of_questionaire_questions_ids')
	question_type = QuestionTypeSerializer()
	question_possible_answers = QuestionPossibleAnswerSerializer()

	class Meta:
		model = Question
		fields = ("total_number_of_questionaire_questions","list_of_questionaire_questions_ids","question_id","question_type","question_title","question_text", "question_possible_answers")

	def get_total_number_of_questionaire_questions(self,obj):
		if obj.no_yaps_in_stream_questionaire_flag == True:
			total_number_of_questionaire_questions = Question.objects.filter(is_active=True,no_yaps_in_stream_questionaire_flag=True).count()
		else:
			total_number_of_questionaire_questions = Question.objects.filter(is_active=True,no_yaps_in_stream_questionaire_flag=False).count()
		return total_number_of_questionaire_questions

	def get_list_of_questionaire_questions_ids(self,obj):
		if obj.no_yaps_in_stream_questionaire_flag == True:
			list_of_questionaire_questions = Question.objects.filter(is_active=True,no_yaps_in_stream_questionaire_flag=True)
			list_of_questionaire_questions_ids = []
			for questionaire_question in list_of_questionaire_questions:
				list_of_questionaire_questions_ids.append(questionaire_question.pk)
			return list_of_questionaire_questions_ids

		else:
			list_of_questionaire_questions = Question.objects.filter(is_active=True,no_yaps_in_stream_questionaire_flag=False)
			list_of_questionaire_questions_ids = []
			for questionaire_question in list_of_questionaire_questions:
				list_of_questionaire_questions_ids.append(questionaire_question.pk)
			return list_of_questionaire_questions_ids




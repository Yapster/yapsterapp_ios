from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from operator import attrgetter
from django.contrib.gis.db import models

class QuestionType(models.Model):
	question_type_id = models.AutoField(primary_key=True)
	question_type_name = models.CharField(max_length=255,unique=True)
	question_type_description = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

class QuestionPossibleAnswer(models.Model):
	question_possible_answer_id = models.AutoField(primary_key=True)
	question_possible_answer_text = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

class Question(models.Model):
	question_id = models.AutoField(primary_key=True)
	question_type = models.ForeignKey(QuestionType)
	question_title = models.CharField(max_length=255)
	question_text = models.CharField(max_length=255)
	question_possible_answers = models.ManyToManyField(QuestionPossibleAnswer,blank=True,null=True)
	no_yaps_in_stream_questionaire_flag = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

class Answer(models.Model):
	answer_id = models.AutoField(primary_key=True)
	user_answer_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="answers")
	chosen_answer = models.ForeignKey(QuestionPossibleAnswer,related_name="answers")
	answer_rank_flag = models.BooleanField(default=False)
	answer_rank = models.BigIntegerField(blank=True,null=True)
	question = models.ForeignKey(Question,related_name="answers")
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	def save(self, *args, **kwargs):
		if not self.pk:
			self.user_reyap_id = Answer.objects.filter(user=self.user).count() + 1
		super(Answer, self).save(*args, **kwargs)
		no_yap_in_stream_questionaire_questions = Question.objects.filter(is_active=True,no_yaps_in_stream_questionaire_flag=True)
		no_yap_in_stream_questionaire_completed = True
		for no_yap_in_stream_questionaire_question in no_yap_in_stream_questionaire_questions:
			if no_yap_in_stream_questionaire_completed == False:
				break
			answers_for_this_question = Answer.objects.filter(user=self.user,question__no_yaps_in_stream_questionaire_flag=True,question=no_yap_in_stream_questionaire_question,is_active=True)
			if len(answers_for_this_question) > 0:
				continue
			else:
				no_yap_in_stream_questionaire_completed = False
		if no_yap_in_stream_questionaire_completed == True:
			#signals.no_yap_in_stream_questionaire_completed.send(sender=sender.__class__,user=self.user)
			pass
		else:
			pass














from rest_framework.response import Response
from rest_framework.decorators import api_view
from notification.serializers import NotificationSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from report.models import *
from django.utils import timezone
from yapster_utils import check_session

class ReportYap(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user,kwargs.pop('session_id'))
		if check[1]:
			kwargs['user'] = user
			kwargs['reported_yap'] = Yap.objects.get(pk=kwargs.pop('reported_yap_id'))
			kwargs['reported_yap_flag'] = True
			Report.objects.create(**kwargs)
			return Response ({"valid":True,"Message":"Yap has successfully been reported."})
		else:
			return Reponse(check[0])

class ReportReyap(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user,kwargs.pop('session_id'))
		if check[1]:
			kwargs['user'] = user
			kwargs['reported_reyap'] = Yap.objects.get(pk=kwargs.pop('reported_reyap_id'))
			kwargs['reported_reyap_flag'] = True
			Report.objects.create(**kwargs)
			return Response ({"valid":True,"Message":"Reyap has successfully been reported."})
		else:
			return Reponse(check[0])

class ReportUser(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user,kwargs.pop('session_id'))
		if check[1]:
			kwargs['user'] = user
			kwargs['reported_user'] = User.objects.get(pk=kwargs.pop('reported_user_id'))
			kwargs['reported_user_flag'] = True
			Report.objects.create(**kwargs)
			return Response ({"valid":True,"Message":"User has successfully been reported."})
		else:
			return Reponse(check[0])

class ReportBug(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user,kwargs.pop('session_id'))
		if check[1]:
			kwargs['user'] = user
			kwargs['reported_bug_flag'] = True
			Report.objects.create(**kwargs)
			return Response ({"valid":True,"Message":"Bug has successfully been reported."})
		else:
			return Reponse(check[0])

class ReportGeneral(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user,kwargs.pop('session_id'))
		if check[1]:
			kwargs['user'] = user
			kwargs['reported_general_flag'] = True
			Report.objects.create(**kwargs)
			return Response ({"valid":True,"Message":"General report has been reported."})
		else:
			return Response(check[0])
		
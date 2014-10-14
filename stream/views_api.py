from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import PostSerializer,StreamMenuSerializer,StreamYapSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from yapster_utils import check_session
from stream.models import *
from yapster_utils import yap_trending_score
from itertools import chain
from operator import attrgetter
import datetime

class LoadStream(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				stream = user.functions.load_stream(request['amount'],request['after'])
				serialized = PostSerializer(stream,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
			else:
				stream = user.functions.load_stream(request['amount'])#,request['after'])
				serialized = PostSerializer(stream,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
		else:
			return Response(check[0])

class LoadStreamMenu(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			serialized = StreamMenuSerializer(user,data=self.request.DATA)
			return Response(serialized.data)
		else:
			return Response(check[0])

class LoadTrendingStream(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			minutes = 2880
			time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
			if 'after' in request:
				yaps = Yap.objects.filter(is_active=True,is_private=False,pk__lt=request['after'],date_created__gte=time)[:request.get('amount')]
			else:
				yaps = Yap.objects.filter(is_active=True,is_private=False,date_created__gte=time)[:request.get('amount')]
			final_yaps = sorted(set(yaps),key=yap_trending_score, reverse=True)
			serialized = StreamYapSerializer(final_yaps,data=self.request.DATA,many=True,context={'user':user})
			return Response(serialized.data)
		else:
			return Response(check[0])

class LoadChannelStream(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			channel_id = request.get('channel_id')
			if 'after' in request:
				yaps = Yap.objects.filter(is_active=True,is_private=False,pk__lt=request['after'],channel__channel_id=channel_id)[:request.get('amount')]
			else:
				yaps = Yap.objects.filter(is_active=True,is_private=False,channel__channel_id=channel_id)[:request.get('amount')]
			final_yaps = sorted(set(yaps),key=attrgetter('date_created'), reverse=True)
			serialized = StreamYapSerializer(final_yaps,data=self.request.DATA,many=True,context={'user':user})
			return Response(serialized.data)
		else:
			return Response(check[0])

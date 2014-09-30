from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import PostSerializer,StreamMenuSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from yapster_utils import check_session
from stream.models import *
from yapster_utils import yap_trending_score

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
				yaps = Yap.objects.filter(is_active=True,is_private=False,pk__lt=after,date_created__gte=time)[:kwargs.get('amount')]
				return sorted(set(yaps),key=yap_trending_score, reverse=True)

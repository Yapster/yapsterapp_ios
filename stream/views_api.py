from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import PostSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from yapster_utils import check_session
from stream.models import *

class LoadStream(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		print request
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
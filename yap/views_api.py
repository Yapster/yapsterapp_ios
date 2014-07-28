from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from yapster_utils import check_session
from users.models import *
from users.serializers import PushNotificationObjectSerializer
from yap.serializers import *

class CreateYap(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if kwargs.get('user_tags_flag') == True:
				user_tags = kwargs.pop('user_tags',[])
				print ("user_tags",user_tags)
			if kwargs.get('hashtags_flag') == True:
				hashtags = kwargs.pop('hashtags',[])
				print ("hashtags", hashtags)
			if kwargs.get('channel_flag'):
				print (kwargs['channel_flag'], "channel_flag")
				kwargs['channel'] = Channel.objects.get(pk=kwargs.pop('channel_id'))
			kwargs['user'] = user
			print kwargs
			yap = Yap.objects.create(**kwargs)
			if kwargs.get('user_tags_flag') == True:
				yap.add_user_tags(user_tags)
			if kwargs.get('hashtags_flag') == True:
				yap.add_hashtags(hashtags)
			return Response({"valid":True,"message":"Yap has successfully been created.","yap_id":yap.pk})
		else:
			return Response(check[0])

class DeleteYap(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			yap = Yap.objects.get(pk=kwargs['yap_id'])
			response = yap.delete(is_user_deleted=False)
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class DeleteReyap(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			reyap = Reyap.objects.get(pk=kwargs['reyap_id'])
			response = reyap.delete(is_user_deleted=True)
			return Response({"valid":True,"message":response})

class FollowRequest(APIView):
	def post(self,request):
		print 1
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print UserFunctions
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			print 2
			#print user.functions
			response = user.functions.follow_request(kwargs['user_requested_id'])
			print 3
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class FollowUnfollow(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			#print user.functions
			response = user.functions.follow_unfollow(kwargs['user_unfollowed_id'])
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class FollowUnrequest(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			#print user.functions
			response = user.functions.follow_unrequest(kwargs['user_requested_id'])
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])


class FollowAccept(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print UserFunctions
		print kwargs
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			#print user.functions
			response = user.functions.follow_accept(kwargs['user_requesting_id'])
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class FollowDeny(APIView):

	def post(self,request):
		print 1
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print UserFunctions
		print kwargs
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			print 2
			#print user.functions
			response = user.functions.follow_deny(kwargs['user_requesting_id'])
			print 3
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class LikeObj(APIView):

	def post(self,request):
		"""example json
		"""
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			if kwargs['obj_type'] == "yap":
				obj = Yap.objects.get(pk=kwargs['obj'])
			else:
				obj = Reyap.objects.get(pk=kwargs['obj'])
			response = user.functions.like(obj,listen,kwargs['time_clicked'])
			if isinstance(response,dict):
				return Response(response)
			else:
				return Response({"valid":True})
		else:
			return Response({"valid":True,"message":check[0]})

class UnlikeObj(APIView):

	def post(self,request):
		"""example json
		"""
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			if kwargs['obj_type'] == "yap":
				obj = Yap.objects.get(pk=kwargs['obj'])
				listen = Listen.objects.get(pk=kwargs['listen_id'])
			else:
				obj = Reyap.objects.get(pk=kwargs['obj'])
				listen = Listen.objects.get(pk=kwargs['listen_id'])
			response = user.functions.unlike(obj,listen,kwargs['time_clicked'])
			if isinstance(response,dict):
				return Response({"valid":False,"message":response})
			else:
				return Response({"valid":True,"message":"success","like_id":response})
		else:
			return Response(check[0])


class ReyapObj(APIView):

	def post(self,request):
		"""example json
		"""
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			if kwargs['obj_type'] == "yap":
				o = Yap.objects.get(pk=kwargs['obj'])
			else:
				o = Reyap.objects.get(pk=kwargs['obj'])
			response = user.functions.reyap(o,listen,kwargs['time_clicked'])
			if isinstance(response,dict):
				return Response({"valid":False,"message":response})
			else:
				return Response({"valid":True,"message":"success","reyap_id":response.pk})
		else:
			return Response(check[0])


class UnreyapObj(APIView):

	def post(self,request):
		"""example json
		"""
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			print listen.pk
			if kwargs['obj_type'] == "yap":
				obj = Yap.objects.get(pk=kwargs['obj'])
				print obj.pk
			else:
				print "It's a reyap"
				obj = Reyap.objects.get(pk=kwargs['obj'])
				print obj.pk
			response = user.functions.unreyap(obj,user,listen,kwargs['time_clicked'])
			print response
			if isinstance(response,str):
				return Response({"valid":False,"message":response})
			elif isinstance(response,bool):
				return Response({"valid":True})
		else:
			return Response(check[0])


class ListenToAnObj(APIView):

	def post(self,request):
		"""example json
		"""
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			if kwargs['obj_type'] == "yap":
				obj = Yap.objects.get(pk=kwargs['obj'])
			else:
				print 
				obj = Reyap.objects.get(pk=kwargs['obj'])
			if kwargs.get('longitude'):
				longitude = kwargs.pop('longitude')
			if kwargs.get('latitude'):
				latitude = kwargs.pop('latitude')
			if kwargs.get('longitude') and kwargs.get('latitude'):
				response = user.functions.listen(obj=obj,longitude=longitude,latitude=latitude)
			else:
				response = user.functions.listen(obj)
			if isinstance(response,dict):
				return Response(response)
			else:
				return Response({"valid":True,"message":"Success","Listen_id":response.pk})
		else:
			return Response(check[0])

class ListenTimeListened(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			response = listen.set_time_listened(time_listened=kwargs['time_listened'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])


class ListenHashtagClicked(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			try:
				hashtag_clicked=Hashtag.objects.get(hashtag_name=kwargs['hashtag_clicked'])
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"This hashtag doesn't exist."})
			listen_click = ListenClick.objects.create(user=user,listen=listen,hashtag_clicked_flag=True,hashtag_clicked=hashtag_clicked,time_clicked=kwargs['time_clicked'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class ListenUserHandleClicked(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			try:
				user_handle_clicked=User.objects.get(username=kwargs['user_handle_clicked'])
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"There is no User with this user handle."})
			listen_click = ListenClick.objects.create(user=user,listen=listen,user_handle_clicked_flag=True,user_handle_clicked=user_handle_clicked,time_clicked=kwargs['time_clicked'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class ListenUserYappedClicked(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			listen_click = ListenClick.objects.create(user=user,listen=listen,user_yapped_clicked_flag=True,time_clicked=kwargs['time_clicked'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class ListenUserReyappedClicked(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			listen_click = ListenClick.objects.create(user=user,listen=listen,user_reyapped_clicked_flag=True,time_clicked=kwargs['time_clicked'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class ListenPictureClicked(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			listen_click = ListenClick.objects.create(user=user,listen=listen,picture_clicked_flag=True,time_clicked=kwargs['time_clicked'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class ListenSkipClicked(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			listen_click = ListenClick.objects.create(user=user,listen=listen,skipped_flag=True,time_clicked=kwargs['time_clicked'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class LoadExploreChannels(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=(request['user_id']))
		check = check_session(user=user,session_id=request['session_id'])
		if check[1]:
			channels = Channel.objects.all()
			serialized = ExploreChannelListSerializer(channels,data=self.request.DATA)
			return Response(serialized.data)
		else:
			return Response(check[0])

class LoadYapChannels(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=(request['user_id']))
		check = check_session(user=user,session_id=request['session_id'])
		if check[1]:
			channels = Channel.objects.all()
			serialized = YapChannelListSerializer(channels,data=self.request.DATA)
			return Response(serialized.data)
		else:
			return Response(check[0])

class ListOfFollowingAndFollowers(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			if 'after' in request:
				list_of_following_and_followers = user.functions.list_of_following_and_followers(amount=request['amount'],after=request['after'])
			else:
				list_of_following_and_followers = user.functions.list_of_following_and_followers(amount=request['amount'])
			serialized = ListOfFollowingAndFollowersSerializer(list_of_following_and_followers,data=self.request.DATA,many=True,context={'user':user})
			return Response(serialized.data)
		else:
			return Response(check[0])

class PushNotificationObjectCall(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		obj = request['obj']
		obj_type = request['obj_type']
		if check[1]:
			if obj_type == "yap":
				try:
					result = Yap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This yap does not exist.'})
			elif obj_type == "reyap":
				try:
					result = Reyap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This reyap does not exist.'})
			serialized = PushNotificationObjectSerializer(result,data=self.request.DATA,context={'user':user})
			return Response(serialized.data)
		else:
			print check
			return Response(check[0])


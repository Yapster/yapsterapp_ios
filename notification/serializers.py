from rest_framework import serializers
from yap.serializers import *
from notification.models import *
from django.contrib.auth.models import User

class NotificationTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = NotificationType
		exclude = ["is_active","origin_yap_flag","origin_yap","origin_reyap_flag","origin_reyap","created_like_flag","created_like","created_reyap_flag","created_reyap","created_listener_request_flag","created_listener_request","created_listen_flag","created_listen","is_yapster_notification","manual_override","override_description"] #Front end doesn't need to know if it's active. The fact that they're receiving it means it's active.

class SingleNotificationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Notification
		exclude = ["is_active","origin_yap_flag","origin_yap","origin_reyap_flag","origin_reyap","created_like_flag","created_like","created_reyap_flag","created_reyap","created_listener_request_flag","created_listener_request","created_listen_flag","created_listen","user_viewed_date","user_clicked_flag","user_clicked_date","manual_override","override_description"] #Front end doesn't need to know if it's active. The fact that they're receiving it means it's active.

class AbstractNotificationSerializer(serializers.ModelSerializer):
	liked_by_viewer = serializers.SerializerMethodField('get_liked_by_viewer')
	listened_by_viewer = serializers.SerializerMethodField('get_listened_by_viewer')
	reyapped_by_viewer = serializers.SerializerMethodField('get_reyapped_by_viewer')
	reyap_flag = serializers.SerializerMethodField('get_reyap_flag')
	reyap_id = serializers.SerializerMethodField('get_reyap_id')
	reyap_user = serializers.SerializerMethodField('get_reyap_user')
	date_created = serializers.SerializerMethodField('get_date_created')


	class Meta:
		model = Yap
		fields = ("reyap_flag","reyap_id","reyap_user","liked_by_viewer","listened_by_viewer","reyapped_by_viewer","date_created")
	
	def get_date_created(self,obj):
		return self.context['date_action_done']

	def get_reyap_id(self,obj):
		user = self.context['user']
		reyap_user = self.context['reyap_user']
		if reyap_user != None:
			if Reyap.objects.filter(yap=obj,user=reyap_user,is_active=True).exists():
				return Reyap.objects.get(yap=obj,user=reyap_user,is_active=True).pk
			else:
				return None
		elif reyap_user == None:
			return None

	def get_reyapped_by_viewer(self,obj):
		user = self.context['user']
		return Reyap.objects.filter(yap=obj,user=user,is_active=True).exists()

	def get_liked_by_viewer(self, obj):
		user = self.context['user']
		return Like.objects.filter(yap=obj,user=user,is_active=True).exists()

	def get_listened_by_viewer(self, obj):
		user = self.context['user']
		return Listen.objects.filter(yap=obj,user=user,is_active=True).exists()

	def get_reyap_user(self, obj):
		user = self.context['user']
		reyap_user = self.context['reyap_user']
		if reyap_user != None:
			if Reyap.objects.filter(yap=obj,user=reyap_user,is_active=True).exists():
				reyap_user = Reyap.objects.get(yap=obj,user=reyap_user,is_active=True).user
				return UserSerializer(reyap_user).data
			else:
				return None
		elif reyap_user == None:
			return None

	def get_reyap_flag(self,obj):
		reyap_flag = self.context['reyap_flag']
		return reyap_flag

class NotificationSerializer(serializers.Serializer):
	
	notification_id = serializers.SerializerMethodField('get_notification_id')
	notification_type = NotificationTypeSerializer()
	notification_info = serializers.SerializerMethodField('get_notification_info')
	notification_created_info = serializers.SerializerMethodField('get_notification_created_info')
	
	def get_notification_id(self, obj):
		if obj.is_active ==True:
			return obj.notification_id
		else:
			return None

	def get_notification_type(self,obj):
		if obj.is_active == True:
			return NotificationTypeSerializer(context={"notification_type_id":obj.notification_type_id,"notification_name":obj.notification_name,"notification_picture_path":obj.notification_picture_path,"notification_message":obj.notification_message}).data
		else:
			return None

	def get_notification_info(self,obj):
		if obj.is_active == True:
			if obj.new_facebook_friend_joined_yapster_flag == True:
				#New Facebook Friend Joined Yapster
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "new_facebook_friend_joined_yapster_flag":obj.new_facebook_friend_joined_yapster_flag}
			elif obj.facebook_friend_newly_connected_to_facebook_flag == True:
				#Facebook Friend Newly Connected To Yapster
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "facebook_friend_newly_connected_to_facebook_flag":obj.facebook_friend_newly_connected_to_facebook_flag}
			elif obj.first_yap_notification_to_all_followers_flag == True:
				#First Yap Notification To All Followers
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "first_yap_notification_to_all_followers_flag":obj.first_yap_notification_to_all_followers_flag}
			elif obj.user_verified_flag == True:
				#Verified Notification
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "user_verified_flag":obj.user_verified_flag}
			elif obj.user_unverified_flag == True:
				#Unverified Notification
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "user_unverified_flag":obj.user_unverified_flag}
			elif obj.user_recommended_flag == True:
				#Recommended Notification
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "user_recommended_flag":obj.user_recommended_flag}
			elif obj.user_unrecommended_flag == True:
				#Unrecommended Notification
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "user_unrecommended_flag":obj.user_unrecommended_flag}
			elif obj.origin_yap_flag == True and obj.created_like_flag == True:
				#Yap Liked
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "origin_yap_flag":obj.origin_yap_flag, "origin_yap":YapSerializer(obj.origin_yap).data, "created_like_flag":obj.created_like_flag, "created_like":LikeSerializer(obj.created_like).data}
			elif obj.origin_yap_flag == True and obj.created_reyap_flag == True:
				#Yap Reyapped
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "origin_yap_flag":obj.origin_yap_flag, "origin_yap":YapSerializer(obj.origin_yap).data, "created_reyap_flag":obj.created_reyap_flag, "created_reyap":ReyapSerializer(obj.created_reyap).data}
			elif obj.origin_yap_flag == True and obj.created_listen_flag == True:
				#Yap Listened
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "origin_yap_flag":obj.origin_yap_flag, "origin_yap":YapSerializer(obj.origin_yap).data,"created_listen_flag":obj.created_listen_flag, "created_listen":ListenSerializer(obj.created_listen).data}
			elif obj.origin_reyap_flag == True and obj.created_like_flag == True:
				#Reyap Liked
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "origin_reyap_flag":obj.origin_reyap_flag, "origin_reyap":ReyapSerializer(obj.origin_reyap).data, "created_like_flag":obj.created_like_flag, "created_like":LikeSerializer(obj.created_like).data}
			elif obj.origin_reyap_flag == True and obj.created_reyap_flag == True:
				#Reyap Reyapped
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "origin_reyap_flag":obj.origin_reyap_flag, "origin_reyap":ReyapSerializer(obj.origin_reyap).data, "created_reyap_flag":obj.created_reyap_flag, "created_reyap":ReyapSerializer(obj.created_reyap).data}
			elif obj.origin_reyap_flag == True and obj.created_listen_flag == True:
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "origin_reyap_flag":obj.origin_reyap_flag, "origin_reyap":ReyapSerializer(obj.origin_reyap).data, "created_listen_flag":obj.created_listen_flag, "created_listen":ListenSerializer(obj.created_listen).data}
			elif obj.created_follower_request_flag == True:
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created, "created_follower_request_flag":obj.created_follower_request_flag, "created_follower_request":FollowerRequestSerializer(obj.created_follower_request).data}
			else:
				return {"user_notification_id":obj.user_notification_id, "user_read_flag":obj.user_read_flag, "user":obj.user, "acting_user":UserSerializer(obj.acting_user).data, "date_created":obj.date_created,  "origin_yap_flag":obj.origin_yap_flag, "origin_yap":YapSerializer(obj.origin_yap).data}
		else:
			return None

	def get_notification_created_info(self,obj):
		if obj.created_like_flag == True or obj.created_reyap_flag == True or obj.created_listen_flag == True:
				if obj.created_listen_flag == True:
					if obj.created_listen.reyap_flag == True:
						return AbstractNotificationSerializer(obj.created_listen.yap,context={'reyap_flag':True,'reyap_user':obj.created_listen.reyap.user,"user":self.context['user'],"date_action_done":obj.date_created}).data
					elif obj.created_listen.reyap_flag == False:
						return AbstractNotificationSerializer(obj.created_listen.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
				if obj.created_like_flag == True:
					if obj.created_like.reyap_flag == True:
						return AbstractNotificationSerializer(obj.created_like.yap,context={'reyap_flag':True,'reyap_user':obj.created_like.reyap.user,"user":self.context['user'],"date_action_done":obj.date_created}).data
					elif obj.created_like.reyap_flag == False:
						return AbstractNotificationSerializer(obj.created_like.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
				if obj.created_reyap_flag == True:
					if obj.created_reyap.reyap_flag == True:
						return AbstractNotificationSerializer(obj.created_reyap.yap,context={'reyap_flag':True,'reyap_user':obj.created_reyap.user,"user":self.context['user'],"date_action_done":obj.date_created}).data
					elif obj.created_reyap.reyap_flag == False:
						return AbstractNotificationSerializer(obj.created_reyap.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		elif obj.notification_type.notification_name == "user_tag":
			return AbstractNotificationSerializer(obj.origin_yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		else:
			return 'None'

	





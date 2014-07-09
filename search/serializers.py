from rest_framework import serializers
from users.models import Profile,Settings,Recommended
from users.serializers import *
from search.models import *
from location.serializers import *
from django.contrib.auth.models import User

class ExploreSearchResultsSerializer(serializers.Serializer):
	yap_id = serializers.SerializerMethodField("get_post_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_post_id(self, obj):
		return obj.yap_id

	def get_post_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return AbstractPostSerializer(obj,context={'reyap_flag':None,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data

	def get_yap_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return YapSerializer(obj).data

class ExplorePeopleSearchSerializer(serializers.ModelSerializer):
	following_info = serializers.SerializerMethodField("get_user_following_info")
	profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
	profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
	user_following_listed_user = serializers.SerializerMethodField("get_user_following_listed_user")

	class Meta:
		model = User
		fields = ("id","username","first_name","last_name","profile_picture_path","profile_cropped_picture_path","user_following_listed_user")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path
	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

	def get_user_following_listed_user(self,obj):
		user = self.context['user']
		if obj.pk == user.pk:
			return None
		else:
			if obj.pk in user.functions.list_of_following():
				user_following_listed_user = True
			else:
				user_following_listed_user = False
			return user_following_listed_user


class ProfileSearchResultsSerializer(serializers.Serializer):
	date_created = serializers.SerializerMethodField("get_date_created")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_date_created(self, obj):
		return obj.date_created

	def get_post_info(self,obj):
		name = obj.__class__.name()
		if name != "yap" and name != "reyap":
			if obj.reyap_flag == True:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.reyap.user,"user":self.context['user'],"date_action_done":obj.date_created}).data
			else:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		elif name == "yap":
			return AbstractPostSerializer(obj,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		else:
			return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.user,"user":self.context['user'],"date_action_done":obj.date_created}).data

	def get_yap_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return YapSerializer(obj).data
		else:
			return YapSerializer(obj.yap).data

class StreamSearchResultsSerializer(serializers.Serializer):
	user_post_id = serializers.SerializerMethodField("get_user_post_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_user_post_id(self, obj):
		return obj.pk

	def get_post_info(self,obj):
		name = obj.__class__.name()
		if name != "yap" and name != "reyap":
			if obj.reyap_flag == True:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.reyap.user,"user":self.context['user'],"date_action_done":obj.date_created}).data
			else:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		elif name == "yap":
			return AbstractPostSerializer(obj,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		else:
			return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.user,"user":self.context['user'],"date_action_done":obj.date_created}).data

	def get_yap_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return YapSerializer(obj).data
		else:
			return YapSerializer(obj.yap).data
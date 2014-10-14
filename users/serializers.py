from rest_framework import serializers
from users.models import *
from yap.models import *
from location.serializers import *
from yap.serializers import YapSerializer
from search.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField('get_profile_picture_path')
	profile_cropped_picture_path = serializers.SerializerMethodField('get_profile_cropped_picture_path')

	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_path

	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

class EditProfileUserSerializer(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField('get_profile_picture_path')
	profile_cropped_picture_path = serializers.SerializerMethodField('get_profile_cropped_picture_path')
	email = serializers.SerializerMethodField('get_profile_email')
	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path","email")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_path

	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path
	def get_profile_email(self,obj):
		return obj.email

class ListUserSerializer(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
	profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
	description = serializers.SerializerMethodField("get_description")

	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path","description")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path
	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

	def get_description(self,obj):
		return obj.profile.description

class RecommendedSerializer(serializers.ModelSerializer):

	user = ListUserSerializer()

	class Meta:
		model = Recommended
		fields = ("user",)

class SettingsSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Settings
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

class AbstractPostSerializer(serializers.ModelSerializer):
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

class PostSerializer(serializers.Serializer):
	post_id = serializers.SerializerMethodField("get_post_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_post_id(self, obj):
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

class StreamYapSerializer(serializers.Serializer):
	yap_id = serializers.SerializerMethodField("get_post_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_post_id(self, obj):
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
		return YapSerializer(obj).data

class ProfileInfoSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True) #not return all info in this
	following_info = serializers.SerializerMethodField("get_following_info")
	user_city = CitySerializer()
	user_country = CountrySerializer()
	user_us_state = USStateSerializer()
	user_us_zip_code = USZIPCodeSerializer()
	last_user_yap_id = serializers.SerializerMethodField("get_last_user_yap_id")
	facebook_connection_flag = serializers.SerializerMethodField("get_facebook_connection_flag")
	facebook_account_id = serializers.SerializerMethodField("get_facebook_account_id")
	facebook_page_connection_flag = serializers.SerializerMethodField("get_facebook_page_connection_flag")
	facebook_page_id = serializers.SerializerMethodField("get_facebook_page_id")
	twitter_connection_flag = serializers.SerializerMethodField("get_twitter_connection_flag")
	twitter_account_id = serializers.SerializerMethodField("get_twitter_account_id")

	class Meta:
		model = Profile
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

	def get_following_info(self,obj):
		user = self.context['user']
		if obj.user.pk == user.pk:
			return None
		else:
			if obj.user.pk in user.functions.list_of_following():
				user_following_profile_user = True
			else:
				user_following_profile_user = False
			if user.pk in obj.user.functions.list_of_following():
				profile_user_following_user = True
			else:
				profile_user_following_user = False
			if obj.user.functions.is_requested_by_the_viewing_user(user_viewing=user) == True:
				user_requested_profile_user = True
			else:
				user_requested_profile_user = False
			return {
				"user_following_profile_user":user_following_profile_user,
				"user_requested_profile_user":user_requested_profile_user,
				"profile_user_following_user":profile_user_following_user,
			}
	def get_last_user_yap_id(self,obj):
		return obj.user.functions.last_user_yap_id

	def get_facebook_connection_flag(self,obj):
		return obj.user.settings.facebook_connection_flag
	def get_facebook_account_id(self,obj):
		if obj.user.settings.facebook_connection_flag == True:
			return obj.user.settings.facebook_account_id
		else:
			return None
	def get_facebook_page_connection_flag(self,obj):
		return obj.user.settings.facebook_page_connection_flag
	def get_facebook_page_id(self,obj):
		if obj.user.settings.facebook_page_connection_flag == True:
			return obj.user.settings.facebook_page_id
		else:
			return None
	def get_twitter_connection_flag(self,obj):
		return obj.user.settings.twitter_connection_flag
	def get_twitter_account_id(self,obj):
		if obj.user.settings.twitter_connection_flag == True:
			return obj.user.settings.twitter_account_id
		else:
			return None

class EditProfileInfoSerializer(serializers.ModelSerializer):
	user = EditProfileUserSerializer(partial=True) #not return all info in this
	user_city = CitySerializer()
	user_country = CountrySerializer()
	user_us_state = USStateSerializer()
	user_us_zip_code = USZIPCodeSerializer()

	class Meta:
		model = Profile
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

class EditUserSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True) #not return all info in this
	user_city = CitySerializer()
	user_country = CountrySerializer()
	user_us_state = USStateSerializer()
	user_us_zip_code = USZIPCodeSerializer()

	class Meta:
		model = UserInfo
		
class ProfileStreamSerializer(serializers.Serializer):
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_post_info(self,obj):
		name = obj.__class__.name()
		if name != "yap" and name != "reyap":
			if obj.reyap_flag == True:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':UserSerializer(obj.reyap.user).data,"user":self.context['user'],"date_action_done":obj.date_created}).data
			else:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		elif name == "yap":
			return AbstractPostSerializer(obj,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		else:
			return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':UserSerializer(obj.user).data,"user":self.context['user'],"date_action_done":obj.date_created}).data

	def get_yap_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return YapSerializer(obj).data
		else:
			return YapSerializer(obj.yap).data

#Profile Stream Serializer for Posts

class ProfilePostStreamSerializer(serializers.Serializer):
	post_date_created = serializers.SerializerMethodField("get_post_date_created")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_post_date_created(self, obj):
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

class ProfileLikeStreamSerializer(serializers.Serializer):
	like_id = serializers.SerializerMethodField("get_like_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_like_id(self,obj):
		return obj.like_id

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

class ProfileListenStreamSerializer(serializers.Serializer):
	listen_id = serializers.SerializerMethodField("get_listen_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_listen_id(self,obj):
		return obj.listen_id

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
	'''
	def get_yap(self,obj):
		try:
			print obj.pk
			yap = obj.yap
			profile_user = obj.user
			return YapSerializer(yap,context={"profile_user":profile_user}).data
		except:
			return None
	def get_reyap(self,obj):
		try:
			reyap = obj.reyap
			profile_user = obj.user
			return ReyapSerializer(reyap,context={"profile_user":profile_user}).data
		except:
			return None

	'''

class PushNotificationObjectSerializer(serializers.Serializer):
	object_id = serializers.SerializerMethodField("get_object_id")
	object_info = serializers.SerializerMethodField("get_object_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_object_id(self, obj):
		return obj.pk

	def get_object_info(self,obj):
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

class StreamMenuSerializer(serializers.Serializer):
	stream_menu_trending_search_option_flag = serializers.SerializerMethodField("get_stream_menu_trending_search_option_flag")
	stream_menu_last_search_option_flag = serializers.SerializerMethodField("get_stream_menu_last_search_option_flag")
	stream_menu_last_search_option = serializers.SerializerMethodField("get_stream_menu_last_search_option")
	stream_menu_list_of_channels = serializers.SerializerMethodField("get_stream_menu_list_of_channels")

	def get_stream_menu_trending_search_option_flag(self,obj):
		return True

	def get_stream_menu_last_search_option_flag(self,obj):
		if Search.objects.filter(is_active=True,user_searching=obj).exists() == True:
			return True
		else:
			return False

	def get_stream_menu_last_search_option(self,obj):
		if Search.objects.filter(is_active=True,user_searching=obj,explore_searched_flag=True).exists() == True:
			search_object = Search.objects.filter(is_active=True,user_searching=obj,explore_searched_flag=True).last()
			if search_object.hashtags_searched_flag == True and search_object.user_handles_searched_flag == False and search_object.channels_searched_flag == False:
				return {"search_type":"hashtags_search", "hashtags_searched":search_object.hashtags_searched.values_list('hashtag_name',flat=True)}
			elif search_object.hashtags_searched_flag == False and search_object.user_handles_searched_flag == True and search_object.channels_searched_flag == False:
				return {"search_type":"user_handles_search", "user_handles_searched":search_object.user_handles_searched.values_list('username',flat=True)}
			elif search_object.hashtags_searched_flag == True and search_object.user_handles_searched_flag == True and search_object.channels_searched_flag == False:
				return {"search_type":"hashtags_search_and_user_handles_search", "hashtags_searched":search_object.hashtags_searched.values_list('hashtag_name',flat=True),"user_handles_searched":search_object.user_handles_searched.values_list('username',flat=True)}
			elif search_object.general_searched_flag == True and search_object.channels_searched_flag == False:
				return {"search_type":"text_search", "text_searched":search_object.text_searched}
			elif search_object.hashtags_searched_flag == True and search_object.user_handles_searched_flag == False and search_object.channels_searched_flag == True:
				return {"search_type":"channels_search_and_hashtags_search", "hashtags_searched":search_object.hashtags_searched.values_list('hashtag_name',flat=True), "channels_searched":search_object.channels_searched.values_list('channel_id',flat=True)}
			elif search_object.hashtags_searched_flag == False and search_object.user_handles_searched_flag == True and search_object.channels_searched_flag == True:
				return {"search_type":"channels_search_and_user_handles_search", "user_handles_searched":search_object.user_handles_searched.values_list('username',flat=True), "channels_searched":search_object.channels_searched.values_list('channel_id',flat=True)}
			elif search_object.hashtags_searched_flag == True and search_object.user_handles_searched_flag == True and search_object.channels_searched_flag == True:
				return {"search_type":"channels_search_and_hashtags_search_and_user_handles_search", "hashtags_searched":search_object.hashtags_searched.values_list('hashtag_name',flat=True),"user_handles_searched":search_object.user_handles_searched.values_list('username',flat=True), "channels_searched":search_object.channels_searched.values_list('channel_id',flat=True)}
			elif search_object.general_searched_flag == True and search_object.channels_searched_flag == True:
				return {"search_type":"channels_and_general_search", "text_searched":search_object.text_searched, "channels_searched":search_object.channels_searched.all()}
		else:
			return None

	def get_stream_menu_list_of_channels(self,obj):
		return Channel.objects.filter(is_active=True).values('channel_id','channel_name')

class StreamYapSerializer(serializers.Serializer):
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




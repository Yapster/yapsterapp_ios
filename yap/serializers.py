from rest_framework import serializers
from users.models import Profile
from yap.models import *
from location.serializers import *
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

class ListUserSerializer(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
	profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
	description = serializers.SerializerMethodField("get_description")

	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path","description")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_path

	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

	def get_description(self,obj):
		return obj.profile.description

class ChannelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Channel
		exclude = ["date_activated","date_deactivated","is_active","manual_override","manual_override_description","icon_explore_path_clicked","icon_explore_path_unclicked","icon_yap_path_clicked","icon_yap_path_unclicked"]

class YapChannelListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Channel
		exclude = ["icon_explore_path_clicked","icon_explore_path_unclicked","date_activated","date_deactivated","is_active","manual_override","manual_override_description"]

class ExploreChannelListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Channel
		exclude = ["icon_yap_path_clicked","icon_yap_path_unclicked","date_activated","date_deactivated","is_active","manual_override","manual_override_description"]

class HashtagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Hashtag
		exclude = ["is_active","is_blocked"]

class YapSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True)
	hashtags = HashtagSerializer()
	channel = ChannelSerializer()
	user_tags = UserSerializer(partial=True)

	class Meta:
		model = Yap

class InternalReyapSerializer(serializers.ModelSerializer):
	yap = YapSerializer()
	reyapped_from = serializers.SerializerMethodField('reyapped_from')

	class Meta:
		model = Reyap
		exclude = ["reyap_reyap","reyap_flag","is_active","manual_override","manual_override_description"]

	def reyapped_from(self,obj):
		if obj.reyap_flag:
			return UserSerializer(obj.reyap.user)
		else:
			return UserSerializer(obj.yap.user)

	def liked_by(self, obj):
		profile_user = obj.profile_user #maybe request.user...check this
		reyap = Reyap.objects.get(pk=obj.pk)
		return Like.objects.filter(yap=reyap.yap,user=profile_user,is_unliked=False,is_active=True).exists()

	def listened_by(self, obj):
		profile_user = obj.profile_user #maybe request.user...check this
		reyap = Reyap.objects.get(pk=obj.pk)
		return Listen.objects.filter(yap=reyap.yap,user=profile_user,is_active=True).exists()

	def reyapped_by(self, obj):
		profile_user = obj.profile_user #maybe request.user...check this
		reyap = Reyap.objects.get(pk=obj.pk)
		return Reyap.objects.filter(yap=reyap.yap,user=profile_user,is_unreyapped=False,is_active=True).exists()

class ReyapSerializer(serializers.ModelSerializer):
	yap = YapSerializer()
	reyapped_from = serializers.SerializerMethodField('reyapped_from')
	reyap_reyap = InternalReyapSerializer()

	class Meta:
		model = Reyap

	def reyapped_from(self,obj):
		if obj.reyap_flag:
			return UserSerializer(obj.reyap.user)
		else:
			return UserSerializer(obj.yap.user)

	def liked_by(self, obj):
		profile_user = obj.profile_user #maybe request.user...check this
		reyap = Reyap.objects.get(pk=obj.pk)
		return Like.objects.filter(yap=reyap.yap,user=profile_user,is_unliked=False,is_active=True).exists()

	def listened_by(self, obj):
		profile_user = obj.profile_user #maybe request.user...check this
		reyap = Reyap.objects.get(pk=obj.pk)
		return Listen.objects.filter(yap=reyap.yap,user=profile_user,is_active=True).exists()

	def reyapped_by(self, obj):
		profile_user = obj.profile_user #maybe request.user...check this
		reyap = Reyap.objects.get(pk=obj.pk)
		return Reyap.objects.filter(yap=reyap.yap,user=profile_user,is_unreyapped=False,is_active=True).exists()

class LikeSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True)
	yap = YapSerializer()
	reyap = ReyapSerializer()

	class Meta:
		model = Like
		exclude = ["is_active","manual_override","manual_override_description"]

class ListenSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True)
	yap = YapSerializer()
	reyap = ReyapSerializer()

	class Meta:
		model = Listen
		exclude = ["is_active","manual_override","manual_override_description"]

class FollowerRequestSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True)
	user_requested = UserSerializer(partial=True)

	class Meta:
		model = FollowerRequest
		exclude = ["is_active","manual_override","manual_override_description"]


class ListOfFollowersSerializer(serializers.ModelSerializer):
	user = ListUserSerializer(partial=True) #not return all info in this
	user_requested = UserSerializer(partial=True)
	profile_user_following = serializers.SerializerMethodField("get_user_following_info")

	class Meta:
		model = FollowerRequest

	def get_user_following_info(self,obj):
		profile_user = self.context['profile_user']
		if obj.user.pk == profile_user.pk:
			return None
		else:
			if obj.user.pk in profile_user.functions.list_of_followers():
				profile_user_following_user = True
			else:
				profile_user_following_user = False
			if profile_user.pk in obj.user.functions.list_of_followers():
				user_following_profile_user = True
			else:
				user_following_profile_user = False
			return {
				"user_following_profile_user":user_following_profile_user,
				"profile_user_following_user":profile_user_following_user
			}


class ListOfFollowingSerializer(serializers.ModelSerializer):
	user = ListUserSerializer(partial=True) #not return all info in this
	user_requested = UserSerializer(partial=True)
	profile_user_following = serializers.SerializerMethodField("get_user_following_info")

	class Meta:
		model = FollowerRequest

	def get_user_following_info(self,obj):
		profile_user = self.context['profile_user']
		if obj.user.pk == profile_user.pk:
			return None
		else:
			if obj.user.pk in profile_user.functions.list_of_following():
				profile_user_following_user = True
			else:
				viewer_following_to_user = False
			if profile_user.pk in obj.user.functions.list_of_following():
				user_following_profile_user = True
			else:
				user_following_profile_user = False
			return {
				"user_following_profile_user":user_following_profile_user,
				"profile_user_following_user":profile_user_following_user
			}

class ListOfFollowingAndFollowersSerializer(serializers.ModelSerializer):
	user = ListUserSerializer(partial=True) #not return all info in this
	user_requested = ListUserSerializer(partial=True)
	relationship_type = serializers.SerializerMethodField("get_relationship_type") 

	class Meta:
		model = FollowerRequest

	def get_relationship_type(self,obj):
		user = self.context['user']
		if obj.user == user:
			return "following"
		elif obj.user_requested == user:
			return "follower"
		else:
			return None

class YapDetailsListOfLikersAndReyappers(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
	profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
	description = serializers.SerializerMethodField("get_description")
	viewing_user_following_user_listed = serializers.SerializerMethodField("get_viewing_user_following_user_listed")

	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path","description","viewing_user_following_user_listed")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_path

	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

	def get_description(self,obj):
		return obj.profile.description

	def get_viewing_user_following_user_listed(self,obj):
		user = self.context['user']
		if obj.pk == user.pk:
			return None
		else:
			if user.pk in obj.functions.list_of_followers():
				return True
			else:
				return False

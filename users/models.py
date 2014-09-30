from django.db import models
from location.models import *
from yap.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from itertools import chain
from operator import attrgetter
from users.signals import *
from django.conf import settings
from django.contrib.gis.db import models
from questionaire.models import *
import string
import random
import signals
import ast
import datetime

class DeactivatedUserLog(models.Model):
	deactivated_user_log_id = models.AutoField(primary_key=True)
	user_deactivated_user_log_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="deactivate_user_logs")
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		if not self.pk:
			self.user_deactivate_user_log_id = DeactivateUserLog.objects.filter(user=self.user).count() + 1
		super(DeactivateUserLog, self).save(*args, **kwargs)

	def delete(self):
		raise NotImplementedError('ManualOverride objects cannot be deleted.')

class BlackList(models.Model):
	blacklist_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=255,unique=True)
	account_created_flag = models.BooleanField(default=False)
	account_created_date = models.DateTimeField(blank=True,null=True)
	blacklisted_date = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	
	def delete(self):
		raise NotImplementedError('BlackList objects cannot be deleted.')


class Profile(models.Model):
	
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other'),
	)

	user = models.OneToOneField(User,primary_key=True,related_name="profile")
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	follower_count = models.BigIntegerField(default=0)
	following_count = models.BigIntegerField(default=0)
	yap_count = models.BigIntegerField(default=0)
	like_count = models.BigIntegerField(default=0)
	listen_count = models.BigIntegerField(default=0)
	reyap_count = models.BigIntegerField(default=0)
	description = models.CharField(blank=True,max_length=255)
	profile_picture_flag = models.BooleanField(default=False)
	profile_picture_path = models.CharField(blank=True,max_length=255)
	profile_picture_cropped_flag = models.BooleanField(default=False)
	profile_picture_cropped_path = models.CharField(blank=True,max_length=255)
	date_of_birth = models.DateField(null=True,blank=True)
	user_city = models.ForeignKey(City,related_name="profile_user_city",null=True,blank=True)
	user_us_state = models.ForeignKey(USState,related_name="profile_user_state",null=True,blank=True)
	user_us_zip_code = models.ForeignKey(USZIPCode,related_name="profile_user_zip_code",null=True,blank=True)
	user_country = models.ForeignKey(Country,related_name="profile_user_country",null=True,blank=True)
	phone_number = models.CharField(max_length=20, blank=True)
	high_security_account_flag = models.BooleanField(default=False)
	verified_account_flag = models.BooleanField(default=False)
	listen_stream_public = models.BooleanField(default=True)
	posts_are_private = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete a profile, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This profile is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'

	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a profile, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'Profile is already activated.'

	def verify_user(self):
		if not self.verified_account_flag:
			self.verified_account_flag = True
			self.save(update_fields=['verified_account_flag'])
		else:
			return False

	def unverify_user(self):
		if self.verified_account_flag:
			self.verified_account_flag = False
			self.save(update_fields=['verified_account_flag'])
		else:
			return False

class UserInfo(models.Model):

	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other'),
	)

	user_id = models.BigIntegerField(primary_key=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
	email = models.EmailField()
	phone_number = models.CharField(max_length=20, blank=True)
	username = models.CharField(max_length=30,unique=True)
	date_of_birth = models.DateField()
	user_city = models.ForeignKey(City,related_name="user_city",blank=True,null=True)
	user_us_state = models.ForeignKey(USState,related_name="user_state",blank=True,null=True)
	user_us_zip_code = models.ForeignKey(USZIPCode,related_name="user_zip_code",blank=True,null=True)
	user_country = models.ForeignKey(Country,related_name="user_country",blank=True,null=True)
	last_account_modified_date = models.DateTimeField(auto_now_add=True)
	high_security_account_flag = models.BooleanField(default=False)
	verified_account_flag = models.BooleanField(default=False)
	facebook_connection_flag = models.BooleanField(default=False)
	facebook_account_id = models.BigIntegerField(blank=True,null=True)
	facebook_share_reyap = models.BooleanField(default=True)
	twitter_connection_flag = models.BooleanField(default=False)
	twitter_account_id = models.BigIntegerField(blank=True,null=True)
	twitter_share_reyap = models.BooleanField(default=True)
	google_plus_connection_flag = models.BooleanField(default=False)
	google_plus_account_id = models.BigIntegerField(blank=True,null=True)
	google_plus_share_reyap = models.BooleanField(default=True)
	linkedin_connection_flag = models.BooleanField(default=False)
	linkedin_account_id = models.BigIntegerField(blank=True,null=True)
	linkedin_share_reyap = models.BooleanField(default=True)
	profile_picture_flag = models.BooleanField(default=False)
	profile_picture_path = models.CharField(blank=True,max_length=255)
	profile_picture_cropped_flag = models.BooleanField(default=False)
	profile_picture_cropped_path = models.CharField(blank=True,max_length=255)
	listen_stream_public = models.BooleanField(default=True)
	posts_are_private = models.BooleanField(default=False)
	description = models.CharField(max_length=255, blank=True)
	notify_for_mentions = models.BooleanField(default=True)
	notify_for_reyaps = models.BooleanField(default=True)
	notify_for_likes = models.BooleanField(default=True)
	notify_for_new_followers = models.BooleanField(default=True)
	notify_for_yapster = models.BooleanField(default=True)
	user_created_latitude = models.FloatField(null=True,blank=True)
	user_created_longitude = models.FloatField(null=True,blank=True)
	user_created_point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	user_deleted_date = models.DateField(blank=True,null=True)
	objects = models.GeoManager()

	def save(self,*args,**kwargs):
		is_created = False
		if not self.pk:
			is_created = True
			self.pk = User.objects.get(username=self.username).pk
		super(UserInfo, self).save(*args, **kwargs)
		if is_created:
			signals.account_created.send(sender=self.__class__,info=self,user=User.objects.get(username=self.username))
				
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete UserInfo, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This UserInfo is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a UserInfo, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'UserInfo is already activated.'

	def modify_account(self,**kwargs):
		'''
		the keyword arguments must be named the names of the models or else a value error is raised

		'''
		user = User.objects.get(username=self.username)
		if kwargs.get("current_password"):
			current_password = kwargs.pop("current_password")
			if user.check_password(current_password) == True:
				if kwargs.get("new_password"):
					new_password = kwargs.pop("new_password")
					user.set_password(new_password)
					user.save(update_fields=['password'])
				else:
					return "You must give a new password for this call."
			else:
				return "Your current password was incorrect."

		if kwargs.get("email"):
			email1 = kwargs.pop("email")
			email2 = email1.replace(' ','')
			email = email2.lower()
			kwargs['email'] = email
			if User.objects.filter(email=email).exists():
				return ("This email has already been used.")
		if kwargs.get("username"):
			username1 = kwargs.pop("username")
			username2 = username1.replace(' ','')
			username = username2.lower()
			kwargs['username'] = username
			if User.objects.filter(username=username).exists() == True:
				return 'This username is unavailable.'
			if BlackList.objects.filter(username=username).exists() == True:
				return 'This username is currently unavailable. Please contact Yapster for more information about creating this account.'

		if kwargs.get("user_country_id") == True and not self.user_country.country_name == "United States":
			kwargs['user_us_state'] = ''
		if kwargs.get("user_us_zip_code") == '':
			user_us_zip_code = None
			kwargs['user_us_zip_code'] = user_us_zip_code

		fields = self._meta.get_all_field_names()
		for item in kwargs.iteritems():
			field = item[0]
			change = item[1]
			if field not in fields:
				raise ValueError("%s is not an option for UserInfo" % (field))
			else:
				setattr(self, field, change) 

		posts_are_private_turned_on = False
		posts_are_private_turned_off = False
		if user.profile.posts_are_private == False and self.posts_are_private == True:
			posts_are_private_turned_on = True
			signals.posts_are_private_turned_on.send(sender=self.__class__,user=user)
		elif user.profile.posts_are_private == True and self.posts_are_private == False:
			posts_are_private_turned_off = True
		signals.account_modified.send(sender=self.__class__,user_id=self.user_id,**kwargs)
		if posts_are_private_turned_on == True:
			signals.posts_are_private_turned_on.send(sender=self.__class__,user=user)
		if posts_are_private_turned_off == True:
			signals.posts_are_private_turned_off.send(sender=self.__class__,user=user)
		self.save()
		return True

	def edit_profile_picture(self,**kwargs):
		self.profile_picture_flag = kwargs['profile_picture_flag']
		self.profile_picture_path = kwargs['profile_picture_path']
		self.profile_picture_cropped_flag = kwargs['profile_picture_cropped_flag']
		self.profile_picture_cropped_path = kwargs['profile_picture_cropped_path']
		self.save(update_fields=['profile_picture_flag','profile_picture_path','profile_picture_cropped_flag','profile_picture_cropped_path'])
		signals.profile_picture_edited.send(sender=self.__class__,info=self,user=User.objects.get(username=self.username),profile_picture_flag=self.profile_picture_flag,profile_picture_path=self.profile_picture_path,profile_picture_cropped_flag=self.profile_picture_cropped_flag,profile_picture_cropped_path=self.profile_picture_cropped_path)
		return 'Profile picture edited.'

	def delete_profile_picture(self,**kwargs):
		self.profile_picture_flag = False
		self.profile_picture_path = None
		self.profile_picture_cropped_flag = False
		self.profile_picture_cropped_path = None
		self.save(update_fields=['profile_picture_flag','profile_picture_path','profile_picture_cropped_flag','profile_picture_cropped_path'])
		signals.profile_picture_deleted.send(sender=self.__class__,info=self,user=User.objects.get(username=self.username))
		return 'Profile picture deleted.'

class Settings(models.Model):
	user = models.OneToOneField(User, primary_key=True,related_name="settings")
	notify_for_mentions = models.BooleanField(default=True)
	notify_for_reyaps = models.BooleanField(default=True)
	notify_for_likes = models.BooleanField(default=True)
	notify_for_listens = models.BooleanField(default=True)
	notify_for_new_followers = models.BooleanField(default=True)
	notify_for_yapster = models.BooleanField(default=True)
	facebook_connection_flag = models.BooleanField(default=False)
	facebook_account_id = models.BigIntegerField(blank=True,null=True)
	facebook_share_reyap = models.BooleanField(default=False)
	twitter_connection_flag = models.BooleanField(default=False)
	twitter_account_id = models.BigIntegerField(blank=True,null=True)
	twitter_share_reyap = models.BooleanField(default=False)
	google_plus_connection_flag = models.BooleanField(default=False)
	google_plus_account_id = models.BigIntegerField(blank=True,null=True)
	google_plus_share_reyap = models.BooleanField(default=False)
	linkedin_connection_flag = models.BooleanField(default=False)
	linkedin_account_id = models.BigIntegerField(blank=True,null=True)
	linkedin_share_reyap = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete Settings, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This Settings is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a Settings, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'Settings is already activated.'
	
class Recommended(models.Model):
	recommendation_id = models.AutoField(primary_key=True)
	user_recommendation_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name='recommended')
	date_recommended = models.DateTimeField(auto_now_add=True)
	date_will_be_deactivated = models.DateTimeField(null=True,blank=True)
	date_deactivated = models.DateTimeField(null=True,blank=True)
	geographic_target = models.ForeignKey(GeographicTarget,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)

	def save(self,*args,**kwargs):
		if not self.pk:
			self.user_recommendation_id = Recommended.objects.filter(user=self.user).count() + 1
		super(Recommended, self).save(*args, **kwargs)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete Recommended obect, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This Recommended object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a Recommended object, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This Recommended object is already activated.'

class ForgotPasswordRequest(models.Model):
	forgot_password_id = models.AutoField(primary_key=True)
	user_forgot_password_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="forgot_password_requests")
	user_email = models.EmailField()
	reset_password_security_code = models.CharField(max_length=255,blank=True,null=True)
	reset_password_security_code_used_flag = models.BooleanField(default=False)
	date_used = models.DateTimeField(blank=True,null=True)
	user_signed_in_after_without_using_flag = models.BooleanField(default=False)
	date_signed_in_without_using = models.DateTimeField(blank=True,null=True)
	forgot_password_request_latitude = models.FloatField(null=True,blank=True)
	forgot_password_request_longitude = models.FloatField(null=True,blank=True)
	forgot_password_request_point = models.PointField(srid=4326,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def save(self,*args,**kwargs):
		if not self.pk:
			self.user_forgot_password_id = ForgotPasswordRequest.objects.filter(user=self.user).count() + 1
			length = 10
			possible_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
			randomly_generated_reset_password_security_code = ''.join(random.choice(possible_characters) for _ in range(length))
			self.reset_password_security_code = randomly_generated_reset_password_security_code
			template_html = 'forgot_password_email.html'
			template_text = 'forgot_password_email.txt'
			from_email = settings.DEFAULT_FROM_EMAIL
			subject = 'Yapster Reset Password Security Code'
			html = get_template(template_html)
			text = get_template(template_text)
			user = self.user
			to = user.email
			fgp = self
			d = Context({'user':user,'fgp':fgp})
			text_content = text.render(d)
			html_content = html.render(d)
			msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
		super(ForgotPasswordRequest, self).save(*args, **kwargs)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			self.is_active = False
			self.save(update_fields=['is_active'])
		elif self.is_active == False :
			return 'This object has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
		elif self.is_active == True:
			return 'This object is already activated.'

	def reset_password_security_code_used(self):
		#When a user uses a Forgot password code it gets deleted
		self.reset_password_security_code_used_flag = True
		self.date_used = datetime.datetime.now()
		self.is_active = False
		self.is_user_deleted = True
		self.save(update_fields=['reset_password_security_code_used_flag','date_used','is_active'])
		return True

	def reset_password_security_code_not_used_and_user_signed_in(self):
		#When a user uses a Forgot password code it gets deleted
		self.user_signed_in_after_without_using_flag = True
		self.date_signed_in_without_using = datetime.datetime.now()
		self.is_active = False
		self.is_user_deleted = True
		self.save(update_fields=['user_signed_in_after_without_using_flag','date_signed_in_without_using','is_active','is_user_deleted'])
		return True

class UserFunctions(models.Model):
	user = models.OneToOneField(User, primary_key=True,related_name="functions")
	is_user_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	@classmethod
	def create(self,**kwargs):
		# create all user methods to avoid signals
		# return user_id
		password = kwargs.pop('password')
		username = kwargs["username"]
		email = kwargs["email"]
		if User.objects.filter(username=username).exists():
			return (False,"This username is unavailable.")
		elif User.objects.filter(email=email).exists():
			return (False,"This email has already been used.")
		elif BlackList.objects.filter(username=username).exists():
			return (False,"This username is currently unavailable. Please contact Yapster for more information about creating this account.")
		first_name = kwargs.get("first_name",None)
		last_name = kwargs.get("last_name",None)
		user = User.objects.create_user(email=email,password=password,username=username,first_name=first_name,last_name=last_name)
		session_device_token = kwargs.pop("session_device_token")
		UserInfo.objects.create(**kwargs)
		UserFunctions.objects.create(user=user)
		session = SessionVerification.objects.get_or_create(user=user,session_device_token=session_device_token)
		return (user.pk,user.username,user.first_name,user.last_name,session[0].pk)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete a UserFunctions object, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This UserFunctions object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a UserFunctions, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This UserFunctions is already activated.'

	def original_follow_number(self):
		return 10

	def like(self, obj,listen,time_clicked,longitude=False,latitude=False):
		'''like the yap if it hasn't been liked by the user. Return the like object.'''
		if obj.__class__.name() == "yap":
			like_counts_for_this_object = Like.objects.filter(yap=obj,user=self.user,is_active=True).count
			if like_counts_for_this_object == 1:
				obj = Like.objects.get(yap=obj,user=self.user,is_active=True)
			elif like_counts_for_this_object == 0:
				obj = Like.objects.create(yap=obj,user=self.user,reyap_flag=False,is_active=True)
			elif like_counts_for_this_object >= 2:
				likes_to_unlike = Like.objects.filter(yap=obj,user=self.user,is_active=True)
				for like in likes_to_unlike:
					like.unlike()
				obj = Like.objects.create(yap=obj,user=self.user,reyap_flag=False,is_active=True)
			listen_click = ListenClick.objects.create(user=self.user,listen=listen,liked_flag=True,liked_like=obj,time_clicked=time_clicked)
		else:
			like_counts_for_this_object = Like.objects.filter(yap=obj.yap,reyap=obj,user=self.user,reyap_flag=True, is_active=True).count
			if like_counts_for_this_object == 1:
				obj = Like.objects.get(yap=obj.yap,reyap=obj,user=self.user,reyap_flag=True, is_active=True)
			elif like_counts_for_this_object == 0:
				obj = Like.objects.create(yap=obj.yap,reyap=obj,user=self.user,reyap_flag=True, is_active=True)
			elif like_counts_for_this_object >= 2:
				likes_to_unlike = Like.objects.filter(yap=obj.yap,reyap=obj,user=self.user,reyap_flag=True, is_active=True)
				for like in likes_to_unlike:
					like.unlike()
				obj = Like.objects.create(yap=obj.yap,reyap=obj,user=self.user,reyap_flag=True, is_active=True)
			listen_click = ListenClick.objects.create(user=self.user,listen=listen,liked_flag=True,liked_like=obj,time_clicked=time_clicked)
		return obj

	def unlike(self, obj,listen,time_clicked,is_user_deleted=False,longitude=False,latitude=False):
		'''deletes like. Returns true if like is deleted and false if like does not exists'''
		objs = Like.objects.filter(yap=obj, user=self.user, is_active=True)
		for obj in objs:
			obj.unlike()
			listen_click = ListenClick.objects.create(user=self.user,listen=listen,unliked_flag=True,liked_like=obj,time_clicked=time_clicked)
		return True

	def reyap(self, obj,listen,time_clicked,longitude=False,latitude=False):
		'''like the yap if it hasn't been liked by the user. Return the like object.'''

		if obj.__class__.name() == "yap":
			reyap_counts_for_this_object = Reyap.objects.filter(yap=obj,user=self.user,is_active=True).count
			if reyap_counts_for_this_object == 1:
				obj = Reyap.objects.get(yap=obj,user=self.user,is_active=True)
			elif reyap_counts_for_this_object == 0:
				obj = Reyap.objects.create(yap=obj,user=self.user,reyap_flag=False,is_active=True)
			elif reyap_counts_for_this_object >= 2:
				reyaps_to_unlike = Reyap.objects.filter(yap=obj,user=self.user,is_active=True)
				for reyap in reyaps_to_unlike:
					reyap.unreyap()
				obj = Reyap.objects.create(yap=obj,user=self.user,reyap_flag=False,is_active=True)
			listen_click = ListenClick.objects.create(user=self.user,listen=listen,reyapped_flag=True,reyapped_reyap=obj,time_clicked=time_clicked,is_active=True)
		else:
			reyap_counts_for_this_object = Reyap.objects.filter(yap=obj.yap,reyap_reyap=obj,user=self.user,reyap_flag=True, is_active=True).count
			if reyap_counts_for_this_object == 1:
				obj = Reyap.objects.get(yap=obj.yap,reyap_reyap=obj,user=self.user,reyap_flag=True, is_active=True)
			elif reyap_counts_for_this_object == 0:
				obj = Reyap.objects.create(yap=obj.yap,reyap_reyap=obj,user=self.user,reyap_flag=True, is_active=True)
			elif reyap_counts_for_this_object >= 2:
				reyaps_to_unlike = Reyap.objects.filter(yap=obj.yap,reyap_reyap=obj,user=self.user,reyap_flag=True, is_active=True)
				for reyap in reyaps_to_unlike:
					reyap.unreyap()
				obj = Reyap.objects.create(yap=obj.yap,reyap_reyap=obj,user=self.user,reyap_flag=True, is_active=True)
			listen_click = ListenClick.objects.create(user=self.user,listen=listen,reyapped_flag=True,reyapped_reyap=obj,time_clicked=time_clicked,is_active=True)
		return obj

	def unreyap(self,obj,user,listen,time_clicked,is_user_deleted=False,longitude=False,latitude=False):
		'''Deletes(makes inactive) a reyap. Returns true if deleted and false if there is no such reyap'''
		objs = Reyap.objects.filter(yap=obj, user=self.user, is_active=True)
		for obj in objs:
			obj.unreyap()
			listen_click = ListenClick.objects.create(user=self.user,listen=listen,unreyapped_flag=True,reyapped_reyap=obj,time_clicked=time_clicked,is_active=True)
		return True

	def listen(self, obj,longitude=None,latitude=None):
		'''like the yap if it hasn't been liked by the user. Return the like object.'''
		if obj.__class__.name() == "yap":
			obj = Listen.objects.create(yap=obj,user=self.user,reyap_flag=False) 
		else:
			obj = Listen.objects.create(yap=obj.yap,reyap=obj,user=self.user,reyap_flag=True) 
		return obj

	def recommended_users_to_follow(self):
		if Answer.objects.filter(is_active=True,question__no_yaps_in_stream_questionaire_flag=True,user=self.user).exists():
			pass
		else:
			recommended = Recommended.objects.filter(is_active=True)
		return recommended

	def is_requested_by_the_viewing_user(self,user_viewing):
		try:
			if self.user.requested.filter(is_unrequested=False,is_accepted=False,is_denied=False,is_unfollowed=False,is_active=True,user=user_viewing).exists():
				return True
		except ObjectDoesNotExist:
			return False


	def list_of_followers(self,amount=None,after=None,queryset=False):
		if after is None:
			followers = self.user.requested.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True)[:amount]
		else:
			followers = self.user.requested.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True,pk__lt=after)[:amount]
		if queryset:
			return followers
		else:
			user_ids = []
			for follower in followers:
				user_ids.append(follower.user.pk)
			return user_ids


	def list_of_following(self,amount=None,after=None,queryset=False):
		if after is None:
			followers = self.user.requests.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True)[:amount]
		else:
			followers = self.user.requests.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True,pk__lt=after)[:amount]
		if queryset:
			return followers
		else:
			user_ids = []
			for follower in followers:
				user_ids.append(follower.user_requested.pk)
			return user_ids

	def list_of_following_and_followers(self,amount,after=None):
		if after is None:
			list_of_following = self.user.requests.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True)[:amount]
			list_of_followers = self.user.requested.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True)[:amount]
		else:
			list_of_following = self.user.requests.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True,pk__lt=after)[:amount]
			list_of_followers = self.user.requested.filter(is_unrequested=False,is_accepted=True,is_unfollowed=False,is_active=True,pk__lt=after)[:amount]
		result_list = sorted(set(chain(list_of_following,list_of_followers)),key=attrgetter('user.username','user_requested.username'))[:amount]
		return result_list

	def follow_request(self, user_requested_id):
		requester = self.user
		if requester.pk == user_requested_id:
			return 'You cannot follow yourself'
		try:
			requesting = User.objects.get(pk=user_requested_id)
		except User.DoesNotExist:
			return 'User DoesNotExist'
		request = FollowerRequest.objects.get_or_create(user=requester,user_requested=requesting,is_unrequested=False,is_unfollowed=False,is_active=True)
		if not request[1]:
			if request[0].is_accepted:
				return 'You are already listening to this user.'
			else:
				return 'You have already requested this user, please wait to be accepted.'
		else:
			return 'Success'

	def follow_unfollow(self, user_unfollowed_id):
		user_unfollowed = User.objects.get(pk=user_unfollowed_id)
		try:
			obj = self.user.requests.get(user=self.user,user_requested=user_unfollowed,is_unrequested=False,is_accepted=True,is_denied=False,is_unfollowed=False,is_active=True)
		except FollowerRequest.DoesNotExist:
			return 'This relationship does not exist.'
		obj.unfollow()
		return 'This user has successfully been unfollowed.'


	def follow_accept(self, user_requesting_id):
		user_requesting = User.objects.get(pk=user_requesting_id)
		try:
			obj = self.user.requested.get(user=user_requesting,user_requested=self.user,is_unrequested=False,is_accepted=False,is_denied=False,is_unfollowed=False,is_active=True)
			obj.accept()
			return 'This user has successfully been accepted.'
		except FollowerRequest.DoesNotExist:
			return 'This relationship does not exist.'

	def follow_deny(self, user_requesting_id):
		user_requesting = User.objects.get(pk=user_requesting_id)
		try:
			obj = self.user.requested.get(user=user_requesting, user_requested=self.user,is_unrequested=False,is_accepted=False,is_denied=False,is_unfollowed=False,is_active=True)
			obj.deny()
			return 'This user has successfully been denied.'
		except FollowerRequest.DoesNotExist:
			return 'This relationship does not exist.'

	def follow_unrequest(self,user_requested_id):
		user_requested = User.objects.get(pk=user_requested_id)
		try:
			obj = self.user.requests.get(user=self.user, user_requested=user_requested,is_unrequested=False,is_accepted=False,is_denied=False,is_unfollowed=False,is_active=True)
			obj.unrequest()
			return 'This user has successfully been unrequested.'
		except FollowerRequest.DoesNotExist:
			return 'User never made a request.'


	def load_notifications(self,amount,after=None):
		if after is None:
			return self.user.notifications.filter(is_active=True)[:amount] #[:amount=20]
		else:
			return self.user.notifications.filter(is_active=True,pk__lt=after)[:amount] #[:amount=20]

	def load_unread_notifications(self,amount,after=None):
		if after is None:
			return self.user.notifications.filter(is_active=True,user_read_flag=False)[:amount] #[:amount=20]
		else:
			return self.user.notifications.filter(is_active=True,user_read_flag=False,pk__lt=after)[:amount] #[:amount=20]

	def load_stream(self,amount,after=None):
		if after is None:
			return self.user.stream.filter(is_active=True)[:amount]
		else:
			return self.user.stream.filter(is_active=True,pk__lt=after)[:amount]

	def load_profile_posts(self,amount,after_yap=None,after_reyap=None):
		#after is a datetime
		if after_yap is None and after_reyap is None:
			yaps = Yap.objects.filter(user=self.user,is_active=True)
			reyaps = Reyap.objects.filter(user=self.user,is_active=True)
		elif after_yap is not None and after_reyap is None:
			yaps = Yap.objects.filter(user=self.user,is_active=True,pk__lt=after_yap)
			reyaps = Reyap.objects.filter(user=self.user,is_active=True)
		elif after_yap is None and after_reyap is not None:
			yaps = Yap.objects.filter(user=self.user,is_active=True)
			reyaps = Reyap.objects.filter(user=self.user,is_active=True,pk__lt=after_reyap)
		else:
			yaps = Yap.objects.filter(user=self.user,is_active=True,pk__lt=after_yap)
			reyaps = Reyap.objects.filter(user=self.user,is_active=True,pk__lt=after_reyap)			
		result_list = sorted(chain(reyaps,yaps),key=attrgetter('date_created'), reverse=True)
		return result_list[:int(amount)]

	def load_profile_likes(self,amount,after=None):
		if after is None:
			abc = Like.objects.filter(user=self.user,is_active=True)[:amount]
			return Like.objects.filter(user=self.user,is_active=True)[:amount]
		else:
			return Like.objects.filter(pk__lt=after,user=self.user,is_active=True)[:amount]


	def load_profile_listens(self,amount,after=None):
		if after is None:
			return Listen.objects.filter(user=self.user,is_active=True)[:amount]
		else:
			return Listen.objects.filter(pk__lt=after,user=self.user,is_active=True)[:amount]

	def recommend_user(self,date_will_be_deactivated=None):
		user = self.user
		if user.profile.is_active and user.profile.verified_account_flag and not Recommended.objects.filter(user=user,is_active=True).exists():
			Recommended.objects.create(user=user,date_will_be_deactivated=date_will_be_deactivated)
			user_recommended.send(sender=self, user=user)
		elif not user.profile.verified_account_flag:
			return 'User is not a verified user.'
		elif not user.profile.is_active:
			return 'User is deactivated.'
		elif not user.profile.verified_account_flag and not user.profile.is_active:
			return 'User is not a verified user and is deactivated.'
		elif Recommended.objects.filter(user=user,is_active=True).exists():
			return 'User is already recommended.'
		else:
			return False

	def unrecommend_user(self):
		user = self.user
		if user.profile.is_active and user.profile.verified_account_flag and Recommended.objects.filter(user=user,is_active=True).exists():
			recommended_records = Recommended.objects.filter(user=user,is_active=True)
			for recommended_record in recommended_records:
				recommended_record.is_active = False
				recommended_record.date_deactivated = datetime.datetime.now()
				recommended_record.save(update_fields=['is_active','date_deactivated'])
				user_unrecommended.send(sender=self, user=user)
		elif not user.profile.verified_account_flag:
			return 'User is not a verified user.'
		elif not user.profile.is_active:
			return 'User is deactivated.'
		elif not user.profile.verified_account_flag and not user.profile.is_active:
			return 'User is not a verified user and is deactivated.'
		elif not Recommended.objects.filter(user=user,is_active=True).exists():
			return 'User is not currently recommended.'
		else:
			return False

	def last_user_yap_id(self):
		user = self.user
		return user.yaps.values('user_yap_id')[:1]
			
	def verify_user(self):
		user = self.user
		if user.profile.is_active and not user.profile.verified_account_flag:
			user_profile = Profile.objects.get(user=user,is_active=True)
			user_profile.verify_user()
			user_verified.send(sender=self, user=user)
			return 'This user has been verified.'
		elif user.profile.verified_account_flag:
			return 'This user has already been verified.'
		elif not user.profile.is_active:
			return 'This user has been deactivated.'
		elif not user.profile.verified_account_flag and not user.profile.is_active:
			return 'This user is not verified and has also been deactivated.'
		else:
			return False

	def unverify_user(self):
		user = self.user
		if user.profile.is_active and user.profile.verified_account_flag:
			user_profile = Profile.objects.get(user=user,is_active=True)
			user_profile.unverify_user()
			user_unverified.send(sender=self, user=user)
			return 'This user has been unverified.'
		elif not user.profile.verified_account_flag:
			return 'This user has already been unverified.'
		elif not user.profile.is_active:
			return 'This user has been deactivated.'
		elif not user.profile.verified_account_flag and not user.profile.is_active:
			return 'This user is not verified and has also been deactivated.'
		else:
			return False

	def forgot_password(self):
		user = self.user
	 	forgot_password_user_record = ForgotPassword.objects.get_or_create(user=user,is_active=True)
	 	forgot_password_user_record = forgot_password_user_record[0]
	 	response = forgot_password_user_record.forgot_password()
	 	return response

	def delete_or_deactivated_account(self,latitude=None,longitude=None):
		user = self.user
		try:
			d = DeactivatedUserLog.objects.get(user=user,is_active=True)
		except ObjectDoesNotExist:
			d = DeactivateUserLog.objects.create(user=user,latitude=latitude,longitude=longitude,is_active=True)
		self.delete(is_user_deleted=True)
		signals.account_deleted_or_deactivated.send(sender=self.__class__,user=self.user)
		return True

class SessionVerification(models.Model):
	session_id = models.AutoField(primary_key=True)
	user_session_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="sessions")
	session_device_token = models.CharField(max_length=255,blank=True,null=True)
	session_manually_closed_flag = models.BooleanField(default=False)
	session_logged_out_flag = models.BooleanField(default=False)
	session_timed_out_flag = models.BooleanField(default=False)
	session_created_latitude = models.FloatField(null=True,blank=True)
	sesssion_created_longitude = models.FloatField(null=True,blank=True)
	session_created_point = models.PointField(srid=4326,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	objects = models.GeoManager()

	def save(self,*args,**kwargs):
		if not self.pk:
			is_created = True
			self.user_post_id = SessionVerification.objects.filter(user=self.user).count() + 1
		super(SessionVerification, self).save(*args, **kwargs)

	def check_date(self):
		if (timezone.now() - self.date_created).days >= 1:
			return False
		else:
			return True

	def check_session(self,user,session_id):
		session_id = int(session_id)
		if self.user == user:
			if self.session_id == session_id:
				return True
			else:
				return 'This session_id is incorrect.'
		else:
			return 'This session and user do not match.'

	def automatic_sign_in_check_session_id_and_device_token(self,user,session_device_token):
		if self.check_date() == True:
			if self.user == user:
				if self.session_device_token == session_device_token:
					return True
				else:
					return'The session_id did not match the current active session_id for this user.'
			else:
				return 'This session_id is not for this user.'
		else:
			self.session_timed_out()
			return 'This session_id is timed_out'


	def sign_in_check_session_id_and_device_token(self,session_device_token=None):
		if self.check_date() == True:
			return True
		elif self.check_date() == False:
			self.session_timed_out()
			return False

	def close_session(self):
		self.is_active = False
		self.session_manually_closed_flag = True
		self.save(update_fields=['is_active','session_manually_closed_flag'])

	def session_timed_out(self):
		self.is_active = False
		self.session_timed_out_flag = True
		self.save(update_fields=['is_active','session_timed_out_flag'])

	def sign_out_device(self):
		self.is_active = False
		self.session_logged_out_flag = True
		self.save(update_fields=['is_active','session_logged_out_flag'])

from django.dispatch import receiver

@receiver(signals.account_created)
def create_user_sections(sender, **kwargs):
	info = kwargs.get("info")
	user = kwargs.get("user")
	Profile.objects.create(
		user=user,
		gender=info.gender,
		description=info.description,
		user_city=info.user_city,
		user_us_state=info.user_us_state,
		user_us_zip_code=info.user_us_zip_code,
		user_country=info.user_country,
		phone_number=info.phone_number,
		date_of_birth=info.date_of_birth,
		profile_picture_flag = info.profile_picture_flag,
		profile_picture_path = info.profile_picture_path,
		profile_picture_cropped_flag = info.profile_picture_cropped_flag,
		profile_picture_cropped_path = info.profile_picture_cropped_path,
	)
	Settings.objects.create(
		user = user,
		facebook_connection_flag = info.facebook_connection_flag,
		facebook_account_id = info.facebook_account_id,
		linkedin_connection_flag = info.facebook_connection_flag,
		linkedin_account_id = info.facebook_account_id,
		google_plus_connection_flag = info.facebook_connection_flag,
		google_plus_account_id = info.facebook_account_id,
		twitter_connection_flag = info.facebook_connection_flag,
		twitter_account_id = info.facebook_account_id
	)

@receiver(signals.account_modified)
def modify_information(sender,**kwargs):
	print kwargs
	user_id = kwargs.get('user_id')
	print user_id
	user_obj = User.objects.get(pk=user_id)
	settings = [
		"notify_for_mentions",
		"notify_for_reyaps",
		"notify_for_likes",
		"notify_for_new_followers",
		"notify_for_yapster",
		"facebook_connection_flag",
		"facebook_account_id",
		"facebook_share_reyap",
		"twitter_connection_flag",
		"twitter_account_id",
		"twitter_share_reyap",
		"google_plus_connection_flag",
		"google_plus_account_id",
		"google_plus_share_reyap",
		"linkedin_connection_flag",
		"linkedin_account_id",
		"linkedin_share_reyap",
	]
	settings_changes = []
	settings_obj = user_obj.settings
	profile = [
		"gender",
		"description",
		"profile_picture_flag",
		"profile_picture_path",
		"profile_picture_cropped_flag",
		"profile_picture_cropped_path",
		"date_of_birth",
		"user_city",
		"user_us_state",
		"user_us_zip_code",
		"user_country",
		"phone_number",
		"high_security_account_flag",
		"verified_account_flag",
		"listen_stream_public",
		"posts_are_private",

	]
	profile_obj = user_obj.profile
	profile_changes = []
	user = [
		"first_name",
		"last_name",
		"username",
		"email",
	]
	user_changes = []
	password = ["password"]

	for k,v in kwargs.iteritems():
		if k in user:
			user_changes.append(k)
			setattr(user_obj,k,v)
		elif k in profile:
			profile_changes.append(k)
			setattr(profile_obj,k,v)
		if k in settings:
			settings_changes.append(k)
			setattr(settings_obj,k,v)			
	if profile_changes != []:		
		profile_obj.save(update_fields=profile_changes)
	if settings_changes != []:
		settings_obj.save(update_fields=settings_changes)
	print user_changes
	if user_changes !=[]:
		user_obj.save(update_fields=user_changes)
'''
@receiver(signals.user_edited)
def user_edited(sender,username,**kwargs):
	user_obj = User.objects.get(username=username)
	print user_obj.username
	user = [
		"username",
		"first_name",
		"last_name",
		"email"
	]
	user_changes = []
	for k,v in kwargs.iteritems():
		if k in user:
			user_changes.append(k)
			setattr(user_obj,k,v)
	if user_changes !=[]:
		print 3
		user_obj.save(update_fields=user_changes)

@receiver(signals.profile_edited)
def profile_edited(sender,username,**kwargs):
	user_obj = User.objects.get(username=username)
	print user_obj.username
	profile = [
		"gender",
		"description",
		"profile_picture_flag",
		"profile_picture_path",
		"profile_picture_cropped_flag",
		"profile_picture_cropped_path",
		"date_of_birth",
		"user_city",
		"user_us_state",
		"user_us_zip_code",
		"user_country",
		"phone_number",
		"high_security_account_flag",
		"verified_account_flag",
		"listen_stream_public",
		"posts_are_private",
	]
	profile_obj = user_obj.profile
	profile_changes = []
	
	for k,v in kwargs.iteritems():
		
		if k in profile:
			profile_changes.append(k)
			setattr(profile_obj,k,v)
	print ("profile_changes",profile_changes)

	if profile_changes != []:
		print user_obj.posts_are_private
		print "Here234"
		#if user_obj.posts_are_private == False and kwargs['posts_are_private'] == True:
		#	print ("posts_are_private", kwargs['posts_are_private'])
		#	signals.posts_are_private_turned_on.send(sender=self.__class__,user=user_obj)
		#elif user_obj.posts_are_private == True and kwargs['posts_are_private'] == False:
		#	print ("posts_are_private", kwargs['posts_are_private'])
		#	signals.posts_are_private_turned_off.send(sender=self.__class__,user=user_obj)
		print 1
		profile_obj.save(update_fields=profile_changes)

@receiver(signals.settings_edited)
def settings_edited(sender,username,**kwargs):
	user_obj = User.objects.get(username=username)
	print user_obj.username
	settings = [
		"notify_for_mentions",
		"notify_for_reyaps",
		"notify_for_likes",
		"notify_for_new_followers",
		"notify_for_yapster",
		"facebook_connection_flag",
		"facebook_account_id",
		"facebook_share_reyap"
		"twitter_connection_flag",
		"twitter_account_id",
		"twitter_share_reyap",
		"google_plus_connection_flag",
		"google_plus_account_id",
		"google_plus_share_reyap",
		"linkedin_connection_flag",
		"linkedin_account_id",
		"linkedin_share_reyap"
	]
	settings_changes = []
	settings_obj = user_obj.settings
	for k,v in kwargs.iteritems():
		if k in settings:
			settings_changes.append(k)
			setattr(settings_obj,k,v)
	if settings_changes != []:
		print 2
		settings_obj.save(update_fields=settings_changes)
'''
@receiver(signals.profile_picture_edited)
def profile_picture_edited(sender,**kwargs):
	user = kwargs['user']
	profile_picture_flag = kwargs['profile_picture_flag']
	profile_picture_path = kwargs['profile_picture_path']
	profile_picture_cropped_flag = kwargs['profile_picture_cropped_flag']
	profile_picture_cropped_path = kwargs['profile_picture_cropped_path']

	user.profile.profile_picture_flag = profile_picture_flag
	user.profile.profile_picture_path = profile_picture_path
	user.profile.profile_picture_cropped_flag = profile_picture_cropped_flag
	user.profile.profile_picture_cropped_path = profile_picture_cropped_path
	user.profile.save(update_fields=['profile_picture_flag','profile_picture_path','profile_picture_cropped_flag','profile_picture_cropped_path'])

@receiver(signals.profile_picture_deleted)
def profile_picture_deleted(sender,**kwargs):
	user = kwargs['user']
	user.profile.profile_picture_flag = False
	user.profile.profile_picture_path = None
	user.profile.profile_picture_cropped_flag = False
	user.profile.profile_picture_cropped_path = None
	user.profile.save(update_fields=['profile_picture_flag','profile_picture_path','profile_picture_cropped_flag','profile_picture_cropped_path'])

@receiver(signals.account_deleted_or_deactivated)
def account_deleted_or_deactivated(sender,**kwargs):
	user = kwargs.get('user')
	user.profile.delete(is_user_deleted=True)
	recommendations = user.recommended.filter(is_active=True)
	for recommendation in recommendations:
		recommendation.delete(is_user_deleted=True)
	user.settings.delete(is_user_deleted=True)
	user_info = UserInfo.objects.get(pk=user.pk)
	user_info.delete(is_user_deleted=True)
	user.is_active = False
	user.save(update_fields=['is_active'])


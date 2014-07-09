from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from yap.models import Yap,Reyap
import yap.signals as yap_signals
import users.signals as user_signals

class Stream(models.Model):
	'''table containing each post for each user that goes to their stream'''
	post_id = models.AutoField(primary_key=True)
	user_post_id = models.BigIntegerField(blank=True) #a number corresponding to the number post in an individual users stream
	user = models.ForeignKey(User,related_name="stream")
	user_posted = models.ForeignKey(User,related_name="posted_to",null=True,blank=True)
	yap = models.ForeignKey(Yap,related_name="stream")
	reyap_flag = models.BooleanField(default=False)
	reyap = models.ForeignKey(Reyap, null=True, blank=True,related_name="stream")
	date_created = models.DateTimeField(null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)

	class Meta:
		ordering = ['-date_created']
	#Changed user_posting to user_posted

	@classmethod
	def name(self):
		return "stream"

	def save(self, *args, **kwargs):
		'''overwritten save method to calculate the user_post_id'''
		is_created = False
		if not self.pk:
			is_created = True
			self.user_post_id = Stream.objects.filter(user=self.user).count() + 1
		super(Stream, self).save(*args, **kwargs)
		if is_created:
			if self.reyap_flag:
				self.user_posted = self.reyap.user
				self.date_created = self.reyap.date_created
			else:
				self.user_posted = self.yap.user
				self.date_created = self.yap.date_created
			self.save(update_fields=['user_posted','date_created'])

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
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

from django.dispatch import receiver

@receiver(yap_signals.yap_created)
def yap_to_feeds(sender, **kwargs):
	#get the yap
	yap = kwargs.get("yap")
	#add to feeds
	followers = yap.user.functions.list_of_followers(queryset=True)
	for follower in followers:
		print follower
		Stream.objects.create(yap=yap,user_posted=yap.user,user=follower.user)

@receiver(yap_signals.reyap_created)
def reyap_to_feeds(sender, **kwargs):
	reyap = kwargs.get("reyap")
	followers = reyap.user.functions.list_of_followers(queryset=True)
	for follower in followers:
		Stream.objects.create(yap=reyap.yap,reyap=reyap,user=follower.user,user_posted=reyap.user,reyap_flag=True)

@receiver(yap_signals.first_five_following_followed_make_stream_objects)
def first_five_following_followed_make_stream_objects(sender,**kwargs):
	user = kwargs.get("user")
	first_five_following_yaps = kwargs.get("first_five_following_yaps")
	for yap in first_five_following_yaps:
		Stream.objects.create(yap=yap,user_posted=yap.user,user=user)

@receiver(yap_signals.yap_deleted)
def yap_deleted(sender,**kwargs):
	yap = kwargs.get("yap")
	stream_objects_with_this_yap = Stream.objects.filter(yap=yap,is_active=True)
	for stream_object_with_this_yap in stream_objects_with_this_yap:
		stream_object_with_this_yap()

@receiver(yap_signals.reyap_deleted)
def reyap_deleted(sender,**kwargs):
	reyap = kwargs.get("reyap")
	stream_objects_with_this_reyap = Stream.objects.filter(reyap=reyap,is_active=True)
	for stream_object_with_this_reyap in stream_objects_with_this_reyap:
		stream_object_with_this_reyap()

@receiver(yap_signals.follower_request_deleted)
def follower_request_deleted(sender,**kwargs):
	follower_request = kwargs.get("follower_request")
	try:
		stream_posts_with_these_users = Stream.objects.filter(user=follower_request.user,user_posted=follower_request.user_requested,is_active=True)
	except ObjectDoesNotExist:
		pass

@receiver(user_signals.account_deleted_or_deactivated)
def account_deleted_or_deactivated(sender,**kwargs):
	user = kwargs.get("user")
	stream_objects_with_this_user = Stream.objects.filter(user=user,is_active=True)
	for stream_object_with_this_user in stream_objects_with_this_user:
		stream_object_with_this_user(is_user_deleted=True)




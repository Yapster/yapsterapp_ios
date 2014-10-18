from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import yap.signals as yap_signals
import users.signals as users_signals
from django.db import models
from location.models import *
from django.dispatch import receiver
from operator import attrgetter
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
import re
import signals
import datetime


class Hashtag(models.Model):
	'''hashtag table'''
	hashtag_id = models.AutoField(primary_key=True)
	hashtag_name = models.CharField(max_length=255,unique=True) #name of tag as string
	date_created = models.DateTimeField(auto_now_add=True)
	is_blocked = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.hashtag_name

	def delete(self):
		'''disabling delete'''
		raise NotImplementedError('Tags cannot be deleted.')

class Channel(models.Model):
	'''table of organizational groups'''
	channel_id = models.AutoField(primary_key=True)
	channel_name = models.CharField(max_length=255,unique=True) #name of Channel as string
	channel_description = models.CharField(max_length=255) #description of the Channel
	icon_explore_path_clicked = models.CharField(unique=True,max_length=255) #location icon is stored
	icon_explore_path_unclicked = models.CharField(unique=True,max_length=255) #location icon is stored
	icon_yap_path_clicked = models.CharField(unique=True,max_length=255) #location icon is stored
	icon_yap_path_unclicked = models.CharField(unique=True,max_length=255) #location icon is stored
	is_bonus_channel = models.BooleanField(default=False) #True if the Channel is not one of the originals
	is_promoted = models.BooleanField(default=True)
	geographic_target = models.ForeignKey(GeographicTarget,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deactivated = models.DateTimeField(null=True,blank=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.channel_name

	def delete(self):
		self.is_active = False
		self.date_deactivated = datetime.datetime.now()
		self.save(update_fields=['is_active','date_deactivated'])

class WebsiteLink(models.Model):
	website_link_id = models.AutoField(primary_key=True)
	website_link = models.URLField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.website_link

	def delete(self):
		'''disabling delete'''
		raise NotImplementedError('Tags cannot be deleted.')


class Yap(models.Model):
	yap_id = models.AutoField(primary_key=True)
	user_yap_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="yaps")
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255,blank=True,null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	hashtags_flag = models.BooleanField(default=False)
	hashtags = models.ManyToManyField(Hashtag, related_name="yaps",blank=True,null=True) #foreign key to tags
	channel_flag = models.BooleanField(default=False)
	channel = models.ForeignKey(Channel, blank=True, null=True,related_name="yaps") #foreign key to Channel
	user_tags_flag = models.BooleanField(default=False)
	user_tags = models.ManyToManyField(User,related_name="yaps_in")
	length = models.BigIntegerField() #time in seconds
	listen_count = models.BigIntegerField(default=0)
	reyap_count = models.BigIntegerField(default=0)
	like_count = models.BigIntegerField(default=0)
	website_links_flag = models.BooleanField(default=False)
	website_links = models.ManyToManyField(WebsiteLink, related_name="yaps",blank=True,null=True)
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	audio_path = models.CharField(unique=True, max_length=255) #location of the audio file
	picture_flag = models.BooleanField(default=False)
	picture_path = models.CharField(unique=True, max_length=255,blank=True,null=True)
	picture_cropped_flag = models.BooleanField(default=False)
	picture_cropped_path = models.CharField(blank=True,max_length=255)
	facebook_shared_flag = models.BooleanField(default=False)
	facebook_account_id = models.BigIntegerField(blank=True,null=True)
	twitter_shared_flag = models.BooleanField(default=False)
	twitter_account_id = models.BigIntegerField(blank=True,null=True)
	google_plus_shared_flag = models.BooleanField(default=False)
	google_plus_account_id = models.BigIntegerField(blank=True,null=True)
	linkedin_shared_flag = models.BooleanField(default=False)
	linkedin_account_id = models.BigIntegerField(blank=True,null=True)
	deleted_date = models.DateTimeField(blank=True,null=True)
	deleted_latitude = models.FloatField(null=True,blank=True)
	deleted_longitude = models.FloatField(null=True,blank=True)
	deleted_point = models.PointField(srid=4326,null=True,blank=True)
	is_private = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	@classmethod
	def name(self):
		return "yap"

	def save(self, *args, **kwargs):
		is_created = False
		if not self.pk:
			is_created = True
			self.user_yap_id = Yap.objects.filter(user=self.user).count() + 1
		if self.user.profile.posts_are_private == True:
			self.is_private = True
		super(Yap, self).save(*args, **kwargs)
		if is_created:
			self.user.profile.yap_count += 1
			self.user.profile.save(update_fields=["yap_count"])
			signals.yap_created.send(sender=self.__class__,yap=self) #send signal if just created
			if Yap.objects.filter(user=self.user,is_active=True).count() == 1:
				users_signals.first_yap_notification_to_all_followers.send(sender=self.__class__,yap=self,user=self.user)
			
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.deleted_date = datetime.datetime.now()
				self.save(update_fields=['is_active','is_user_deleted','deleted_date'])
				self.user.profile.yap_count -= 1
				self.user.profile.save(update_fields=["yap_count"])
			elif is_user_deleted == False:
				self.is_active = False
				self.deleted_date = datetime.datetime.now()
				self.save(update_fields=['is_active','deleted_date'])
				self.user.profile.yap_count -= 1
				self.user.profile.save(update_fields=["yap_count"])
			signals.yap_deleted.send(sender=self.__class__,yap=self)
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This yap is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'

	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.deleted_date = None
				self.save(update_fields=['is_active','is_user_deleted','deleted_date'])
			elif is_user_activated == False:
				return 'To activate a yap, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This yap is already activated.'

 	def add_hashtags(self, hashtags):
		if isinstance(hashtags,str):
			#if its a string, separate by a coma with optional whitespace on either side
			hashtags = re.split(r'\s*,\s*',hashtags)
		#try:
		for hashtag in hashtags:
			t = Hashtag.objects.get_or_create(hashtag_name=hashtag)[0] #create the tag
			self.hashtags.add(t) #add the new tag to the foreign key
		#except TypeError:
			#raise TypeError("You can only add tags as a string or list")

	def add_user_tags(self, user_tags,by_id=True):
		if isinstance(user_tags,str):
			#if its a string, separate by a coma with optional whitespace on either side
			user_tags = re.split(r'\s*,\s*',user_tags)
		for user_tag in user_tags:
			try:
				u = User.objects.get(username=user_tag.lower())
				self.user_tags.add(u)
			except User.DoesNotExist:
				return 'This user does not exist'
			return True
		signals.user_tag_notification.send(sender = self.__class__, yap=self)

	def add_website_links(self, website_links):
		for website_link in website_links:
			w = WebsiteLink.objects.get_or_create(website_link=website_link)[0]
			self.website_links.add(w)
			return True

class Reyap(models.Model):
	'''Reyap table'''
	reyap_id = models.AutoField(primary_key=True)
	user_reyap_id = models.BigIntegerField(default=1)
	yap = models.ForeignKey(Yap,related_name='reyaps')
	user = models.ForeignKey(User, related_name='reyaps')
	reyap_flag = models.BooleanField(default=False)
	reyap_reyap = models.ForeignKey("self",blank=True, null=True,related_name="reyaps")
	facebook_connection_flag = models.BooleanField(default=False)
	facebook_account_id = models.BigIntegerField(blank=True,null=True)
	twitter_connection_flag = models.BooleanField(default=False)
	twitter_account_id = models.BigIntegerField(blank=True,null=True)
	google_plus_connection_flag = models.BooleanField(default=False)
	google_plus_account_id = models.BigIntegerField(blank=True,null=True)
	linkedin_connection_flag = models.BooleanField(default=False)
	linkedin_account_id = models.BigIntegerField(blank=True,null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	reyap_count = models.BigIntegerField(default=0)
	like_count = models.BigIntegerField(default=0)
	listen_count = models.BigIntegerField(default=0)
	is_unreyapped = models.BooleanField(default=False)
	unreyapped_date = models.DateTimeField(blank=True,null=True)
	unreyapped_latitude = models.FloatField(null=True,blank=True)
	unreyapped_longitude = models.FloatField(null=True,blank=True)
	unreyapped_point = models.PointField(srid=4326,null=True,blank=True)
	deleted_date = models.DateTimeField(blank=True,null=True)
	deleted_latitude = models.FloatField(null=True,blank=True)
	deleted_longitude = models.FloatField(null=True,blank=True)
	deleted_point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	@classmethod
	def name(self):
		return "reyap"

	def save(self, *args, **kwargs):
		'''save overwritten to increase reyap counts where relevant'''
		is_created = False
		if not self.pk:
			self.user_reyap_id = Reyap.objects.filter(user=self.user).count() + 1
			is_created = True
		super(Reyap, self).save(*args, **kwargs)
		if is_created:
			if self.reyap_flag == False:
				self.yap.reyap_count += 1
				self.yap.save(update_fields=['reyap_count'])
			elif self.reyap_flag == True:
				self.reyap_reyap.reyap_count += 1
				self.reyap_reyap.save(update_fields=['reyap_count'])
				self.yap.reyap_count += 1
				self.yap.save(update_fields=['reyap_count'])
			self.user.profile.yap_count += 1
			self.user.profile.reyap_count += 1
			self.user.profile.save(update_fields=["yap_count","reyap_count"])
			signals.reyap_created.send(sender=self.__class__,reyap=self) #send signal if just created

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.deleted_date = datetime.datetime.now()
				self.save(update_fields=['is_active','is_user_deleted','deleted_date'])
				if self.reyap_flag == False:
					self.yap.reyap_count -= 1
					self.yap.save(update_fields=['reyap_count'])
				elif self.reyap_flag == True:
					self.reyap_reyap.reyap_count -= 1
					self.reyap_reyap.save(update_fields=['reyap_count'])
					self.yap.reyap_count -= 1
					self.yap.save(update_fields=['reyap_count'])
				self.user.profile.yap_count -= 1
				self.user.profile.reyap_count -= 1
				self.user.profile.save(update_fields=["yap_count","reyap_count"])
			elif is_user_deleted == False:
				self.is_active = False
				self.deleted_date = datetime.datetime.now()
				self.save(update_fields=['is_active','deleted_date'])
				if self.reyap_flag == False:
					self.yap.reyap_count -= 1
					self.yap.save(update_fields=['reyap_count'])
				elif self.reyap_flag == True:
					self.reyap_reyap.reyap_count -= 1
					self.reyap_reyap.save(update_fields=['reyap_count'])
					self.yap.reyap_count -= 1
					self.yap.save(update_fields=['reyap_count'])
				self.user.profile.yap_count -= 1
				self.user.profile.reyap_count -= 1
				self.user.profile.save(update_fields=["yap_count","reyap_count"])
			signals.reyap_deleted.send(sender=self.__class__,reyap=self)
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This reyap is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'

	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.deleted_date = None
				self.save(update_fields=['is_active','is_user_deleted','deleted_date'])
				if self.reyap_flag == False:
					self.yap.reyap_count += 1
					self.yap.save(update_fields=['reyap_count'])
				elif self.reyap_flag == True:
					self.reyap_reyap.reyap_count += 1
					self.reyap_reyap.save(update_fields=['reyap_count'])
					self.yap.reyap_count += 1
					self.yap.save(update_fields=['reyap_count'])
				self.user.profile.yap_count += 1
				self.user.profile.reyap_count += 1
				self.user.profile.save(update_fields=["yap_count","reyap_count"])
			elif is_user_activated == False:
				return 'To activate a reyap, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This reyap is already activated.'

	def unreyap(self,is_user_deleted=False,unreyapped_latitude=None,unreyapped_longitude=None):
		self.is_unreyapped = True
		self.unreyapped_date = datetime.datetime.now()
		self.unreyapped_latitude = unreyapped_latitude
		self.unreyapped_longitude = unreyapped_longitude
		if unreyapped_longitude != None and unreyapped_latitude != None:
			self.unreyapped_point = Point(unreyapped_latitude,unreyapped_longitude)
			self.save(update_fields=['is_unreyapped','unreyapped_date','unreyapped_latitude','unreyapped_longitude','unreyapped_point'])
		else:
			self.save(update_fields=['is_unreyapped','unreyapped_date','unreyapped_latitude','unreyapped_longitude'])
		self.delete(is_user_deleted=is_user_deleted)

class Like(models.Model):
	like_id = models.AutoField(primary_key=True)
	user_like_id = models.BigIntegerField(default=1)
	yap = models.ForeignKey(Yap,related_name='likes')
	user = models.ForeignKey(User,related_name='likes')
	reyap_flag = models.BooleanField(default=False)
	reyap = models.ForeignKey(Reyap,blank=True, null=True,related_name='likes')
	date_created = models.DateTimeField(auto_now_add=True)
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	is_unliked = models.BooleanField(default=False)
	unliked_date = models.DateTimeField(null=True,blank=True)
	unliked_latitude = models.FloatField(null=True,blank=True)
	unliked_longitude = models.FloatField(null=True,blank=True)
	unliked_point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	@classmethod
	def name(self):
		return "like"

	def save(self, *args, **kwargs):
		is_created = False
		if not self.pk:
			self.user_like_id = Like.objects.filter(user=self.user).count() + 1
			is_created = True
		super(Like, self).save(*args, **kwargs)
		if is_created:
			if self.reyap_flag == False:
				self.yap.like_count += 1
				self.yap.save(update_fields=['like_count'])
			elif self.reyap_flag == True:
				self.reyap.like_count += 1
				self.reyap.save(update_fields=['like_count'])
				self.yap.like_count += 1
				self.yap.save(update_fields=['like_count'])
			self.user.profile.like_count += 1
			self.user.profile.save(update_fields=["like_count"])
			signals.like_created.send(sender=self.__class__,like=self)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				if self.reyap_flag == False:
					self.yap.like_count -= 1
					self.yap.save(update_fields=['like_count'])
				elif self.reyap_flag == True:
					self.reyap.like_count -= 1
					self.reyap.save(update_fields=['like_count'])
					self.yap.like_count -= 1
					self.yap.save(update_fields=['like_count'])
				self.user.profile.like_count -= 1
				self.user.profile.save(update_fields=["like_count"])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				if self.reyap_flag == False:
					self.yap.like_count -= 1
					self.yap.save(update_fields=['like_count'])
				elif self.reyap_flag == True:
					self.reyap.like_count -= 1
					self.reyap.save(update_fields=['like_count'])
					self.yap.like_count -= 1
					self.yap.save(update_fields=['like_count'])
				self.user.profile.like_count -= 1
				self.user.profile.save(update_fields=["like_count"])
			signals.like_deleted.send(sender=self.__class__,like=self)
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This like object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				if self.reyap_flag == False:
					self.yap.like_count += 1
					self.yap.save(update_fields=['like_count'])
				elif self.reyap_flag == True:
					self.reyap.like_count += 1
					self.reyap.save(update_fields=['like_count'])
					self.yap.like_count += 1
					self.yap.save(update_fields=['like_count'])
				self.user.profile.like_count += 1
				self.user.profile.save(update_fields=["like_count"])
			elif is_user_activated == False:
				return 'To activate a like, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This like is already activated.'

	def unlike(self,is_user_deleted=False,unliked_latitude=None,unliked_longitude=None):
		self.is_unliked = True
		self.unliked_date = datetime.datetime.now()
		self.unliked_latitude = unliked_latitude
		self.unliked_longitude = unliked_longitude
		if unliked_latitude != None and unliked_longitude != None:
			self.unliked_point = Point(unliked_latitude,unliked_longitude)
			self.save(update_fields=['is_unliked','unliked_date','unliked_latitude','unliked_longitude','unliked_point'])
		else:
			self.save(update_fields=['is_unliked','unliked_date','unliked_latitude','unliked_longitude'])
		self.delete(is_user_deleted=is_user_deleted)

class Listen(models.Model):
	'''table for a yap or reyap listen'''
	listen_id = models.AutoField(primary_key=True)
	user_listen_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User, related_name='listens')
	yap = models.ForeignKey(Yap, related_name='listens')
	reyap_flag = models.BooleanField(default=False)
	reyap = models.ForeignKey(Reyap,related_name='listens',blank=True,null=True)
	listen_click_count = models.BigIntegerField(default=0)
	date_created = models.DateTimeField(auto_now_add=True)
	time_listened = models.BigIntegerField(blank=True,null=True) #amount of time listened. defaults to 0 seconds and the `set_time` function can be used to edit
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	@classmethod
	def name(self):
		return "listen"

	def save(self, *args, **kwargs):
		'''overwritten save to increment relevant listen_counts'''
		is_created = False
		if not self.pk:
			self.user_listen_id = Listen.objects.filter(user=self.user).count() + 1
			is_created = True
		super(Listen, self).save(*args, **kwargs)
		if is_created:
			if self.reyap_flag == False:
				self.yap.listen_count += 1
				self.yap.save(update_fields=['listen_count'])
			elif self.reyap_flag == True:
				self.reyap.listen_count += 1
				self.reyap.save(update_fields=['listen_count'])
				self.yap.listen_count += 1
				self.yap.save(update_fields=['listen_count'])
			self.user.profile.listen_count += 1
			self.user.profile.save(update_fields=["listen_count"])
			signals.listen_created.send(sender=self.__class__,listen=self)
	
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				if self.reyap_flag == False:
					self.yap.listen_count -= 1
					self.yap.save(update_fields=['listen_count'])
				elif self.reyap_flag == True:
					self.reyap.listen_count -= 1
					self.reyap.save(update_fields=['listen_count'])
					self.yap.listen_count -= 1
					self.yap.save(update_fields=['listen_count'])
				self.user.profile.listen_count -= 1
				self.user.profile.save(update_fields=["listen_count"])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				if self.reyap_flag == False:
					self.yap.listen_count -= 1
					self.yap.save(update_fields=['listen_count'])
				elif self.reyap_flag == True:
					self.reyap.listen_count -= 1
					self.reyap.save(update_fields=['listen_count'])
					self.yap.listen_count -= 1
					self.yap.save(update_fields=['listen_count'])
				self.user.profile.listen_count -= 1
				self.user.profile.save(update_fields=["listen_count"])
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This listen object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				if self.reyap_flag == False:
					self.yap.listen_count += 1
					self.yap.save(update_fields=['listen_count'])
				elif self.reyap_flag == True:
					self.reyap.listen_count += 1
					self.reyap.save(update_fields=['listen_count'])
					self.yap.listen_count += 1
					self.yap.save(update_fields=['listen_count'])
				self.user.profile.listen_count += 1
				self.user.profile.save(update_fields=["listen_count"])
			elif is_user_activated == False:
				return 'To activate a listen, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This listen is already activated.'

	def set_time_listened(self,time_listened):
		'''change the amount of time listened for'''
		self.time_listened = time_listened
		self.save(update_fields=['time_listened'])
		if self.reyap_flag == True:
			signals.listen_created_on_reyap_time_listened_updated(sender=self.__class__,listen=self)

class ListenClick(models.Model):
	listen_click_id = models.AutoField(primary_key=True)
	user_listen_click_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name='user_listen_clicked')
	listen = models.ForeignKey(Listen,related_name='listen_clicked')
	hashtag_clicked_flag = models.BooleanField(default=False)
	hashtag_clicked = models.ForeignKey(Hashtag,related_name='listen_clicked',null=True,blank=True)
	user_handle_clicked_flag = models.BooleanField(default=False)
	user_handle_clicked = models.ForeignKey(User,related_name='listen_handle_clicked',null=True,blank=True)
	user_yapped_clicked_flag = models.BooleanField(default=False)
	user_reyapped_clicked_flag = models.BooleanField(default=False)
	web_link_clicked_flag = models.BooleanField(default=False)
	picture_clicked_flag = models.BooleanField(default=False)
	skipped_flag = models.BooleanField(default=False)
	liked_flag = models.BooleanField(default=False)
	unliked_flag = models.BooleanField(default=False)
	liked_like = models.ForeignKey(Like,related_name='listens_liked',blank=True,null=True)
	reyapped_flag = models.BooleanField(default=False)
	unreyapped_flag = models.BooleanField(default=False)
	reyapped_reyap = models.ForeignKey(Reyap,related_name='listens_reyapped',blank=True,null=True)
	time_clicked = models.BigIntegerField()
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		is_created = False
		if not self.pk:
			self.user_listen_click_id = ListenClick.objects.filter(user=self.user).count() + 1
			is_created = True
		super(ListenClick, self).save(*args, **kwargs)
		self.listen.listen_click_count += 1
		self.listen.save(update_fields=['listen_click_count'])

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				self.listen.listen_click_count -= 1
				self.listen.save(update_fields=['listen_click_count'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				self.listen.listen_click_count -= 1
				self.listen.save(update_fields=['listen_click_count'])
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This listen_click object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				self.listen.listen_click_count += 1
				self.listen.save(update_fields=['listen_click_count'])
			elif is_user_activated == False:
				return 'To activate a listen_click, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This listen_click is already activated.'

class FollowerRequest(models.Model):
	follower_request_id = models.AutoField(primary_key=True)
	user_follower_request_id = models.BigIntegerField(default=1)
	#user is the person asking to listen
	user = models.ForeignKey(User, related_name='requests')
	#user_requested is the person being asked to be listen to
	user_requested = models.ForeignKey(User, related_name='requested')
	date_created = models.DateTimeField(auto_now_add=True)
	created_latitude = models.FloatField(null=True,blank=True)
	created_longitude = models.FloatField(null=True,blank=True)
	created_point = models.PointField(srid=4326,null=True,blank=True)
	is_unrequested = models.BooleanField(default=False)
	date_unrequested = models.DateTimeField(blank=True,null=True)
	unrequested_latitude = models.FloatField(null=True,blank=True)
	unrequested_longitude = models.FloatField(null=True,blank=True)
	unrequested_point = models.PointField(srid=4326,null=True,blank=True)
	is_accepted = models.BooleanField(default=False)
	date_accepted = models.DateTimeField(null=True,blank=True)
	accepted_latitude = models.FloatField(null=True,blank=True)
	accepted_longitude = models.FloatField(null=True,blank=True)
	accepted_point = models.PointField(srid=4326,null=True,blank=True)
	is_denied = models.BooleanField(default=False)
	date_denied = models.DateTimeField(null=True,blank=True)
	denied_latitude = models.FloatField(null=True,blank=True)
	denied_longitude = models.FloatField(null=True,blank=True)
	denied_point = models.PointField(srid=4326,null=True,blank=True)
	is_unfollowed = models.BooleanField(default=False)
	unfollowed_latitude = models.FloatField(null=True,blank=True)
	unfollwed_longitude = models.FloatField(null=True,blank=True)
	unfollwed_point = models.PointField(srid=4326,null=True,blank=True)
	date_unfollowed = models.DateTimeField(null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	@classmethod
	def name(self):
		return "request"

	def __unicode__(self):
		if self.is_accepted and self.is_active:
			return "%s follows %s" % (self.user, self.user_requested)
		else:
			return "%s wants to follow %s" % (self.user, self.user_requested)

	def save(self, *args, **kwargs):
		is_created = False
		if not self.pk:
			self.user_follower_request_id = FollowerRequest.objects.filter(user=self.user).count() + 1
			is_created = True
		super(FollowerRequest, self).save(*args, **kwargs)
		if is_created:
			if not self.user_requested.profile.posts_are_private:
				#if the user requested is not private, accept the request
				self.accept()
				if len(self.user.requests.filter(is_active=True,is_accepted=True,is_unfollowed=False)) == 5 and self.user.profile.verified_account_flag == False: 
					five_folllower_requests = self.user.requests.filter(is_active=True,is_accepted=True)
					signals.first_five_following_followed_get_yaps.send(sender=self.__class__,user=self.user,five_folllower_requests=five_folllower_requests)
			else:
				signals.follower_requested.send(sender=self.__class__,follower_request=self)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				self.user.profile.following_count -= 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count -= 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				self.user.profile.following_count -= 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count -= 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			signals.follower_request_deleted.send(sender=self.__class__,follower_request=self)
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This FollowerRequest object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			elif is_user_activated == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			signals.follower_request_activated.send(sender=self.__class__,follower_request=self)
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This FollowerRequest is already activated.'

	def unrequest(self):
		self.is_unrequested = True
		if not self.date_unrequested:
			self.date_unrequested = datetime.datetime.now()
			self.is_user_deleted = True
			self.is_active = False
			self.save(update_fields=['is_unrequested','date_unrequested','is_user_deleted','is_active'])
			signals.follower_request_unrequested.send(sender=self.__class__,follower_request=self)

	def accept(self):
		self.is_accepted = True
		if not self.date_accepted:
			self.date_accepted = datetime.datetime.now()
		self.save(update_fields=['date_accepted','is_accepted'])
		self.user.profile.following_count += 1
		self.user.profile.save(update_fields=['following_count'])
		self.user_requested.profile.follower_count += 1
		self.user_requested.profile.save(update_fields=['follower_count'])
		if self.user_requested.profile.posts_are_private:
			signals.follower_accepted.send(sender=self.__class__,follower_request=self)
		else:
			signals.follower_new.send(sender=self.__class__,follower_request=self)

	def deny(self):
		self.is_accepted = False
		if not self.date_denied:
			self.date_denied = datetime.datetime.now()
			self.save(update_fields=['date_denied','is_denied'])

	def unfollow(self):
		self.is_unfollowed = True
		if not self.date_unfollowed:
			self.date_unfollowed = datetime.datetime.now()
			self.is_user_deleted = False
			self.is_active = False
			self.save(update_fields=['date_unfollowed','is_unfollowed','is_active'])
			self.user.profile.following_count -= 1
			self.user.profile.save(update_fields=["following_count"])
			self.user_requested.profile.follower_count -=1
			self.user_requested.profile.save(update_fields=["follower_count"])
			signals.follower_request_unfollowed.send(sender=self.__class__,follower_request=self)


@receiver(yap_signals.first_five_following_followed_get_yaps)
def first_five_following_followed_get_yaps(sender, **kwargs):
	yaps_to_add_to_stream = []
	five_folllower_requests = kwargs.get("five_folllower_requests")
	user = kwargs.get("user")
	for follower_request in five_folllower_requests:
		user = follower_request.user
		user_requested = follower_request.user_requested
		most_recent_five_yaps = user_requested.yaps.filter(is_active=True)[:5]
		yaps_to_add_to_stream.extend(most_recent_five_yaps)
	first_five_following_yaps = sorted(set(yaps_to_add_to_stream),key=attrgetter('date_created'))
	signals.first_five_following_followed_make_stream_objects.send(sender=sender,user=user,first_five_following_yaps=first_five_following_yaps)


@receiver(yap_signals.yap_deleted)
def yap_deleted(sender, **kwargs):
	yap = kwargs.get("yap")
	#Delete All The Listens With This Yap
	listens_with_this_yap = Listen.objects.filter(yap=yap,is_active=True)
	for listen in listens_with_this_yap:
		listen.delete(is_user_deleted=yap.is_user_deleted)
	#Delete All The Likes With This Yap
	likes_with_this_yap = Like.objects.filter(yap=yap,is_active=True)
	for like in likes_with_this_yap:
		like.delete(is_user_deleted=yap.is_user_deleted)
	reyaps_with_this_yap = Reyap.objects.filter(yap=yap,is_active=True)
	for reyap in reyaps_with_this_yap:
		reyap.delete(is_user_deleted=yap.is_user_deleted)

@receiver(yap_signals.reyap_deleted)
def reyap_deleted(sender, **kwargs):
	reyap = kwargs.get("reyap")
	#Delete All The Listens With This Yap
	listens_with_this_reyap = Listen.objects.filter(reyap_flag=True,reyap=reyap,is_active=True)
	for listen in listens_with_this_reyap:
		listen.delete(is_user_deleted=reyap.is_user_deleted)
	#Delete All The Likes With This Yap
	likes_with_this_reyap = Like.objects.filter(reyap_flag=True,reyap=reyap,is_active=True)
	for like in likes_with_this_reyap:
		like.delete(is_user_deleted=reyap.is_user_deleted)
	reyaps_with_this_reyap = Reyap.objects.filter(reyap_flag=True,reyap_reyap=reyap,is_active=True)


@receiver(yap_signals.listen_deleted)
def listen_deleted(sender, **kwargs):
	listen = kwargs.get("listen")
	listen_clicks_with_this_listen = Listen.objects.filter(reyap_flag=True,reyap=reyap,is_active=True)
	for listen_click in listen_clicks_with_this_listen:
		listen_click.delete(is_user_deleted=listen.is_user_deleted)

@receiver(users_signals.account_deleted_or_deactivated)
def account_deleted_or_deactivated(sender,**kwargs):
	user = kwargs.get("user")
	user_yaps = user.yaps.filter(is_active=True)
	user_reyaps = user.reyaps.filter(is_active=True)
	user_likes = user.likes.filter(is_active=True)
	user_listens = user.listens.filter(is_active=True)
	user_follower_requests = user.requests.filter(is_active=True)
	user_follower_requested = user.requested.filter(is_active=True)
	for yap in user_yaps:
		yap.delete(is_user_deleted=True)
	for reyap in user_reyaps:
		reyap.delete(is_user_deleted=True)
	for like in user_likes:
		like.delete(is_user_deleted=True)
	for listen in user_listens:
		listen.delete(is_user_deleted=True)
	for follower_request in user_follower_requests:
		follower_request.delete(is_user_deleted=True)
	for follower_requested in user_follower_requested:
		follower_requested.delete(is_user_deleted=True)





from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import users.signals as users_signals
from django.dispatch import receiver
import yap.signals as yap_signals
from apns import APNs, Payload
from yap.models import *
import datetime
import time

class NotificationType(models.Model):
	notification_type_id = models.AutoField(primary_key=True)
	notification_name = models.CharField(max_length=100,unique=True)
	notification_picture_path = models.CharField(max_length=255,blank=True)
	notification_message = models.CharField(max_length=255,blank=True)
	is_yapster_notification = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	def delete(self,user):
		if self.is_active:
			self.is_active = False
			self.save(update_fields=['is_active'])
			return True
		else:
			return False

	def activate(self):
		if not self.is_active:
			self.is_active = True
			self.save(update_fields=['is_active'])
			return True
		else:
			return False

class Notification(models.Model):
	"""created and origin depends on why the object is sent and where it is sent from"""
	notification_id = models.AutoField(primary_key=True)
	user_notification_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="notifications")
	notification_type = models.ForeignKey(NotificationType,related_name="notifications")
	origin_yap_flag = models.BooleanField(default=False)
	origin_yap = models.ForeignKey(Yap,blank=True,null=True)
	origin_reyap_flag = models.BooleanField(default=False)
	origin_reyap = models.ForeignKey(Reyap,null=True,blank=True)
	acting_user = models.ForeignKey(User,related_name="notifications_sent")
	created_like_flag = models.BooleanField(default=False)
	created_like = models.ForeignKey(Like,blank=True,null=True,related_name="notifications")
	created_reyap_flag = models.BooleanField(default=False)
	created_reyap = models.ForeignKey(Reyap,null=True,blank=True,related_name="notifications")
	created_follower_request_flag = models.BooleanField(default=False)
	created_follower_request = models.ForeignKey(FollowerRequest,null=True,blank=True,related_name="notifications")
	created_listen_flag = models.BooleanField(default=False)
	created_listen = models.ForeignKey(Listen,null=True,blank=True,related_name="notifications")
	is_yapster_notification = models.BooleanField(default=False)
	user_verified_flag = models.BooleanField(default=False)
	user_unverified_flag = models.BooleanField(default=False)
	user_recommended_flag = models.BooleanField(default=False)
	user_unrecommended_flag = models.BooleanField(default=False)
	user_read_flag = models.BooleanField(default=False)
	user_read_date = models.DateTimeField(blank=True,null=True)
	user_clicked_flag = models.BooleanField(default=False)
	user_clicked_date = models.DateTimeField(blank=True,null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)

	class Meta:
		ordering = ['-date_created']

	def save(self,*args,**kwargs):
		if not self.pk:
			self.user_notification_id = Notification.objects.filter(user=self.user).count() + 1
		super(Notification, self).save(*args, **kwargs)

		if not self.date_created:
			if created_reyap_flag:
				self.date_created = self.created_reyap.date_created
			elif created_like_flag:
				self.date_created = self.created_like.date_created
			elif created_follower_request_flag:
				self.date_created = datetime.datetime.now()
			elif created_listen_flag:
				self.date_created = self.created_listen.date_created
			super(Notification, self).save(update_fields=['date_created'])

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

	def read(self):
		self.user_read_flag = True
		self.user_read_date = datetime.datetime.now()
		self.save(update_fields=['user_read_flag','user_read_date'])
		return 'This notification has been read.'
	
	def clicked(self):
		self.user_clicked_flag = True
		self.user_clicked_date = datetime.datetime.now()
		self.save(update_fields=['user_clicked_flag','user_clicked_date'])
		return 'This notification has been clicked.'

@receiver(yap_signals.like_created)
def like_notification(sender, **kwargs):
	like = kwargs.get("like")
	notif_type = NotificationType.objects.get_or_create(notification_name="like_created")[0]
	if like.reyap_flag == True:
		if like.user != like.reyap.user:
			if like.reyap.user.settings.notify_for_likes == True:
				notification = Notification.objects.create(origin_reyap_flag=True,
									origin_reyap=like.reyap,
									created_like_flag=True,
									created_like=like,
									user=like.reyap.user,
									acting_user=like.user,
									notification_type=notif_type,
				)
				try:
					notification
				except NameError:
					pass
				if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
					apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
					#Send a notification
					token_hex1 = notification.user.session.session_udid
					token_hex2 = token_hex1.replace('<','')
					token_hex3 = token_hex2.replace('>','')
					token_hex = token_hex3.replace(' ','')
					print token_hex
					alert = str(acting_user) + " has liked your reyap \"" + like.yap.title + "\"."
					badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
					payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type.notification_name,'user_id':notification.user.pk,'obj_type':'reyap','obj':notification.origin_reyap.pk})
					apns.gateway_server.send_notification(token_hex,payload)


	elif like.reyap_flag == False:
		if like.user != like.yap.user:
			if like.yap.user.settings.notify_for_likes == True:
				notification = Notification.objects.create(origin_yap_flag=True,
									origin_yap=like.yap,
									created_like_flag=True,
									created_like=like,
									user=like.yap.user,
									acting_user=like.user,
									notification_type=notif_type,
				)
				try:
					notification
				except NameError:
					pass
					return "No notfication has been created in the like_created signal."
				if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
					apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
					#Send a notification
					token_hex1 = notification.user.session.session_udid
					token_hex2 = token_hex1.replace('<','')
					token_hex3 = token_hex2.replace('>','')
					token_hex = token_hex3.replace(' ','')
					badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
					alert = "@" + str(notification.acting_user) + " has liked your yap \"" + notification.origin_yap.title + "\"."
					payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type.notification_name,'user_id':notification.user.pk,'obj_type':'yap','obj':notification.origin_yap.pk})
					apns.gateway_server.send_notification(token_hex,payload)


@receiver(yap_signals.reyap_created)
def reyap_notifications(sender, **kwargs):
	reyap = kwargs.get("reyap")
	notif_type = NotificationType.objects.get_or_create(notification_name="reyap_created")[0]
	if reyap.reyap_flag == True:
		if reyap.user != reyap.reyap_reyap.user:
			if reyap.reyap_reyap.user.settings.notify_for_reyaps == True:
				notification = Notification.objects.create(origin_reyap_flag=True,
									origin_reyap=reyap.reyap_reyap,
									created_reyap_flag=True,
									created_reyap=reyap,
									user=reyap.reyap_reyap.user,
									acting_user=reyap.user,
									notification_type=notif_type,
				)

				try:
					notification
				except NameError:
					pass
				if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
					apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
					#Send a notification
					token_hex1 = notification.user.session.session_udid
					token_hex2 = token_hex1.replace('<','')
					token_hex3 = token_hex2.replace('>','')
					token_hex = token_hex3.replace(' ','')
					badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
					alert = "@" + str(notification.acting_user) + " has reyapped your reyap \"" + notification.origin_reyap.title + "\"."
					payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type.notification_name,'user_id':notification.user.pk,'obj_type':'yap','obj':notification.origin_reyap.pk})
					apns.gateway_server.send_notification(token_hex,payload)

	elif reyap.reyap_flag == False:
		if reyap.user != reyap.yap.user:
			if reyap.yap.user.settings.notify_for_reyaps == True:
				notification = Notification.objects.create(origin_yap_flag=True,
									origin_yap=reyap.yap,
									created_reyap_flag=True,
									created_reyap=reyap,
									user=reyap.yap.user,
									acting_user=reyap.user,
									notification_type=notif_type,
				)

				try:
					notification
				except NameError:
					pass
				if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
					apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
					#Send a notification
					token_hex1 = notification.user.session.session_udid
					token_hex2 = token_hex1.replace('<','')
					token_hex3 = token_hex2.replace('>','')
					token_hex = token_hex3.replace(' ','')
					badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
					alert = "@" + str(notification.acting_user) + " has reyapped your yap \"" + notification.origin_yap.title + "\"."
					payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type.notification_name,'user_id':notification.user.pk,'obj_type':'yap','obj':notification.origin_yap.pk})
					apns.gateway_server.send_notification(token_hex,payload)


@receiver(yap_signals.follower_requested)
def been_requested_notification(sender, **kwargs):
	request = kwargs.get("follower_request")
	notif_type = NotificationType.objects.get_or_create(notification_name="follower_requested")[0]
	if request.user_requested.profile.posts_are_private:
		notification = Notification.objects.create(user = request.user_requested,
							acting_user = request.user,
							created_follower_request_flag = True,
							created_follower_request = request,
							notification_type = notif_type
		)

		try:
			notification
		except NameError:
			pass
			apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
		if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
			#Send a notification
			token_hex1 = notification.user.session.session_udid
			token_hex2 = token_hex1.replace('<','')
			token_hex3 = token_hex2.replace('>','')
			token_hex = token_hex3.replace(' ','')
			badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
			alert = "@" + str(notification.acting_user.username) + " has just requested to follow you."
			payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type.notification_name,'user_id':notification.user.pk,'profile_user_id':notification.created_follower_request.user.pk})
			apns.gateway_server.send_notification(token_hex,payload)


@receiver(yap_signals.follower_accepted)
def been_accepted_notification(sender, **kwargs):
	request = kwargs.get("follower_request")
	notif_type = NotificationType.objects.get_or_create(notification_name="follower_accepted")[0]
	if request.user_requested.profile.posts_are_private:
		if request.user_requested.settings.notify_for_new_followers == True:
			notification = Notification.objects.create(user = request.user,
								acting_user = request.user_requested,
								created_follower_request_flag = True,
								created_follower_request = request,
								notification_type = notif_type
			)
			try:
				notification
			except NameError:
				pass
			if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
				apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
				#Send a notification
				token_hex1 = notification.user.session.session_udid
				token_hex2 = token_hex1.replace('<','')
				token_hex3 = token_hex2.replace('>','')
				token_hex = token_hex3.replace(' ','')
				badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
				alert = "@" + str(notification.acting_user.username) + " has just accepted your follow request."
				payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type.notification_name,'user_id':notification.user.pk,'profile_user_id':notification.created_follower_request.user_requested.pk})
				apns.gateway_server.send_notification(token_hex,payload)


@receiver(yap_signals.follower_new)
def new_listener_notification(sender, **kwargs):
	request = kwargs.get("follower_request")
	notif_type = NotificationType.objects.get_or_create(notification_name="new_follower")[0]
	if not request.user_requested.profile.posts_are_private:
		if request.user_requested.settings.notify_for_new_followers == True:
			notification = Notification.objects.create(user = request.user_requested,
								acting_user = request.user,
								created_follower_request_flag = True,
								created_follower_request = request,
								notification_type = notif_type
			)

			try:
				notification
				apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
			except NameError:
				pass
			if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
				#Send a notification
				token_hex1 = notification.user.session.session_udid
				token_hex2 = token_hex1.replace('<','')
				token_hex3 = token_hex2.replace('>','')
				token_hex = token_hex3.replace(' ','')
				badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
				alert = "@" + str(notification.acting_user.username) + " has just followed you."
				payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type.notification_name,'user_id':notification.user.pk,'profile_user_id':notification.created_follower_request.user.pk})
				apns.gateway_server.send_notification(token_hex,payload)


@receiver(yap_signals.user_tag_notification)
def user_tag_notification(sender, **kwargs):
	yap = kwargs.get("yap")
	user_tags = yap.user_tags
	for user in user_tags.all():
		if user != yap.user:
			notif_type = NotificationType.objects.get_or_create(notification_name="user_tag")
			notification = Notification.objects.create(user = user,
				origin_yap_flag = True,
				origin_yap = yap,
				acting_user = yap.user,
				notification_type = notif_type[0]
			)
			try:
				notification
			except NameError:
				pass
			if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
				apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
				#Send a notification
				token_hex1 = user.session.session_udid
				token_hex2 = token_hex1.replace('<','')
				token_hex3 = token_hex2.replace('>','')
				token_hex = token_hex3.replace(' ','')
				alert = str(notification.acting_user.username) + " just tagged you in their yap \"" + notification.origin_yap.title + "\"."
				badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
				payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type[0].notification_name,'user_id':notification.user.pk,'obj_type':'yap','obj':notification.origin_yap.pk})
				apns.gateway_server.send_notification(token_hex,payload)

#User Verified Reciever

@receiver(users_signals.user_verified)
def user_verified_notification(sender, **kwargs):
	user = kwargs.get("user")
	notif_type = NotificationType.objects.get_or_create(notification_name="user_verified")
	notification = Notification.objects.create(user=user, acting_user=user, notification_type=notif_type[0], user_verified_flag=True)

	try:
		notification
	except NameError:
		pass
	if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
		apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
		#Send a notification
		token_hex1 = user.session.session_udid
		token_hex2 = token_hex1.replace('<','')
		token_hex3 = token_hex2.replace('>','')
		token_hex = token_hex3.replace(' ','')
		alert = "Yapster has just verified you."
		badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
		payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type[0].notification_name,'user_id':notification.user.pk,'profile_user_id':notification.user.pk})
		apns.gateway_server.send_notification(token_hex,payload)

#User Unverified Reciever

@receiver(users_signals.user_unverified)
def user_unverified_notification(sender, **kwargs):
	user = kwargs.get("user")
	notif_type = NotificationType.objects.get_or_create(notification_name="user_unverified")
	Notification.objects.create(user=user, acting_user=user, notification_type=notif_type[0], user_unverified_flag=True)

#User_Recommended_Receiver

@receiver(users_signals.user_recommended)
def user_recommended_notification(sender, **kwargs):
	user = kwargs.get("user")
	notif_type = NotificationType.objects.get_or_create(notification_name="user_recommended")
	notification = Notification.objects.create(user=user, acting_user=user, notification_type=notif_type[0], user_recommended_flag=True)
	
	try:
		notification
	except NameError:
		pass
	if notification.user.session.session_udid is not None or notification.user.session.session_udid == "(null)":
		apns = APNs(use_sandbox=True,cert_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_cert_dev.pem',key_file='/home/ec2-user/downloads/yapsterapp_ios/yapster_ios_push_key_dev.pem')
		#Send a notification
		token_hex1 = user.session.session_udid
		token_hex2 = token_hex1.replace('<','')
		token_hex3 = token_hex2.replace('>','')
		token_hex = token_hex3.replace(' ','')
		alert = "Yapster has just made you a recommended user."
		badge_number = Notification.objects.filter(is_active=True,user=notification.user,user_read_flag=False).count()
		payload = Payload(alert=alert,sound="default",badge=badge_number,custom={'notification_type':notif_type[0].notification_name,'user_id':notification.user.pk,'profile_user_id':notification.user.pk})
		apns.gateway_server.send_notification(token_hex,payload)

#User_Unrecommended_Receiver

@receiver(users_signals.user_unrecommended)
def user_unrecommended_notification(sender, **kwargs):
	user = kwargs.get("user")
	notif_type = NotificationType.objects.get_or_create(notification_name="user_unrecommended")
	Notification.objects.create(user=user, acting_user=user, notification_type=notif_type[0], user_unrecommended_flag=True,)

@receiver(yap_signals.yap_deleted)
def yap_deleted(sender, **kwargs):
	yap = kwargs.get("yap")
	user_tags = yap.user_tags.all()
	try:
		notif_type = NotificationType.objects.get(notification_name="user_tag")
	except ObjectDoesNotExist:
		pass
	for user in user_tags:
		try:
			notifications_for_this_yap = Notification.objects.filter(user=user,origin_yap=yap,notif_type=notif_type,is_active=True)
		except ObjectDoesNotExist:
			pass
		for notification in notifications_for_this_yap:
			notification.delete(is_user_deleted=yap.is_user_deleted)

@receiver(yap_signals.reyap_deleted)
def reyap_deleted(sender, **kwargs):
	reyap = kwargs.get("reyap")
	try:
		notif_type = NotificationType.objects.get(notification_name="reyap_created")
	except ObjectDoesNotExist:
		pass
	try:
		notifications_for_this_yap = Notification.objects.filter(created_reyap_flag=True,created_reyap=reyap,notification_type=notif_type,is_active=True)
	except ObjectDoesNotExist:
		pass
	for notification in notifications_for_this_yap:
		notification.delete(is_user_deleted=reyap.is_user_deleted)

@receiver(yap_signals.like_deleted)
def like_deleted(sender, **kwargs):
	like = kwargs.get("like")
	try:
		notif_type = NotificationType.objects.get(notification_name="like_created")
	except ObjectDoesNotExist:
		pass
	try:
		notifications_for_this_yap = Notification.objects.filter(created_like_flag=True,created_like=like,notif_type=notif_type,is_active=True)
	except ObjectDoesNotExist:
		pass
	for notification in notifications_for_this_yap:
		notification.delete(is_user_deleted=like.is_user_deleted)

@receiver(users_signals.account_deleted_or_deactivated)
def account_deleted_or_deactivated(sender, **kwargs):
	user = kwargs.get("user")
	try:
		notifications_for_this_user = Notification.objects.filter(user=user,is_active=True)
	except ObjectDoesNotExist:
		pass
	for notification in notifications_for_this_user:
		notification.delete(is_user_deleted=True)






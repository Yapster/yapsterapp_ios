from django.db import models
from users.models import *
from yap.models import *
from stream.models import *
from notification.models import *
from report.models import *
from search.models import *
from location.models import *

class ManualOverride(models.Model):
	manual_override_id = models.AutoField(primary_key=True)
	user_manual_override_id = models.BigIntegerField(default=1)
	manual_override_description = models.CharField(max_length=255)
	user_override_flag = models.BooleanField(default=False)
	user_override_object = models.ForeignKey(User,related_name="manual_overrides")
	blacklist_override_flag = models.BooleanField(default=False)
	blacklist_override_object = models.ForeignKey(BlackList,related_name="manual_overrides")
	profile_override_flag = models.BooleanField(default=False)
	profile_override_object = models.ForeignKey(Profile,related_name="manual_overrides")
	user_info_override_flag = models.BooleanField(default=False)
	user_info_override_object = models.ForeignKey(UserInfo,related_name="manual_overrides")
	settings_override_flag = models.BooleanField(default=False)
	settings_override_object = models.ForeignKey(Settings,related_name="manual_overrides")
	recommended_override_flag = models.BooleanField(default=False)
	recommended_override_object = models.ForeignKey(Recommended,related_name="manual_overrides")
	forgot_password_request_override_flag = models.BooleanField(default=False)
	forgot_password_request_override_object = models.ForeignKey(ForgotPasswordRequest,related_name="manual_overrides")
	user_functions_override_flag = models.BooleanField(default=False)
	user_functions_override_object = models.ForeignKey(UserFunctions,related_name="manual_overrides")
	session_verification_override_flag = models.BooleanField(default=False)
	session_verification_override_object = models.ForeignKey(SessionVerification,related_name="manual_overrides")
	stream_override_flag = models.BooleanField(default=False)
	stream_override_object = models.ForeignKey(Stream,related_name="manual_overrides")
	hashtag_override_flag = models.BooleanField(default=False)
	hashtag_override_object = models.ForeignKey(Hashtag,related_name="manual_overrides")
	channel_override_flag = models.BooleanField(default=False)
	channel_override_object = models.ForeignKey(Channel,related_name="manual_overrides")
	yap_override_flag = models.BooleanField(default=False)
	yap_override_object = models.ForeignKey(Yap,related_name="manual_overrides")
	reyap_override_flag = models.BooleanField(default=False)
	reyap_override_object = models.ForeignKey(Reyap,related_name="manual_overrides")
	like_override_flag = models.BooleanField(default=False)
	like_override_object = models.ForeignKey(Like,related_name="manual_overrides")
	listen_override_flag = models.BooleanField(default=False)
	listen_override_object = models.ForeignKey(Listen,related_name="manual_overrides")
	listen_click_override_flag = models.BooleanField(default=False)
	listen_click_override_object = models.ForeignKey(ListenClick,related_name="manual_overrides")
	follower_request_override_flag = models.BooleanField(default=False)
	follower_request_override_object = models.ForeignKey(FollowerRequest,related_name="manual_overrides")
	notification_type_override_flag = models.BooleanField(default=False)
	notification_type_override_object = models.ForeignKey(NotificationType,related_name="manual_overrides")
	notification_override_flag = models.BooleanField(default=False)
	notification_override_object = models.ForeignKey(Notification,related_name="manual_overrides")
	search_override_flag = models.BooleanField(default=False)
	search_override_object = models.ForeignKey(Search,related_name="manual_overrides")
	report_override_flag = models.BooleanField(default=False)
	report_override_object = models.ForeignKey(Report,related_name="manual_overrides")
	geographic_target_override_flag = models.BooleanField(default=False)
	geographic_target_override_object = models.ForeignKey(GeographicTarget,related_name="manual_overrides")
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		if not self.pk:
			self.user_manual_override_id = ManualOverride.objects.filter(user=self.user).count() + 1
		super(ManualOverride, self).save(*args, **kwargs)

	def delete(self):
		raise NotImplementedError('ManualOverride objects cannot be deleted.')





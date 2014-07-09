from django.contrib.auth.models import User
from django.db import models
from yap.models import *

class Report(models.Model):
	report_id = models.AutoField(primary_key=True)
	user_report_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="reported")
	reported_yap_flag = models.BooleanField(default=False)
	reported_yap = models.ForeignKey(Yap,null=True,blank=True,related_name="reports")
	reported_reyap_flag = models.BooleanField(default=False)
	reported_reyap = models.ForeignKey(Reyap,null=True,blank=True,related_name="reports")
	reported_user_flag = models.BooleanField(default=False)
	reported_user = models.ForeignKey(User,null=True,blank=True,related_name="reports")
	reported_bug_flag = models.BooleanField(default=False)
	reported_general_flag = models.BooleanField(default=False)
	contact_email = models.EmailField(null=True,blank=True)
	contact_phone_number = models.CharField(max_length=20, null=True,blank=True)
	description = models.CharField(max_length=255,null=True,blank=True)
	datetime_reported = models.DateTimeField(auto_now_add=True)
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)

	def save(self,*args,**kwargs):
		if not self.pk:
			self.user_report_id = Report.objects.filter(user=self.user).count() + 1
		super(Report, self).save(*args, **kwargs)

	def delete(self,is_user_deleted,manual_override_flag=None,manual_override_description=None):
		if manual_override_flag:
			if not self.manual_override_flag:
				self.manual_override_flag = True
				self.save(update_fields=['manual_override_flag'])
				return True 
			else:
				return False
			if not self.override_description:
				self.manual_override_description = manual_override_description
				self.save(update_fields=['manual_override_description'])
			if is_user_deleted:
				if self.is_active:
					self.is_active = False
					self.save(update_fields=['is_active'])
					return True
				else:
					return False
			else:
				return False
		if not manual_override_flag:
			if is_user_deleted:
				if not self.is_user_deleted:
					self.is_user_deleted = True
					self.save(update_fields=['is_user_deleted'])
					return True
				else:
					return False
				if self.is_active:
					self.is_active = False
					self.save(update_fields=['is_active'])
				else:
					return False
			else:
				return False
		else:
			return False

	def activate(self,manual_override_flag,manual_override_description=None):
		if manual_override_flag:
			if not self.manual_override_flag:
				self.manual_override_flag = True
				self.save(update_fields=['manual_override_flag'])
				return True 
			else:
				return False
			if override_description:
				self.manual_override_description = manual_override_description
				self.save(update_fields=['manual_override_description'])
			else:
				return False
			if not self.is_active:
				self.is_active = True
				self.save(update_fields=['is_active'])
				return True
			else:
				return False
		else:
			return False
		if not manual_override_flag:
			if is_user_deleted:
				if not is_user_deleted:
					self.is_user_deleted = False
					self.save(update_fields=['is_user_deleted'])
					return True
				else:
					return False
				if not self.is_active:
					self.is_active = True
					self.save(update_fields=['is_active'])
				else:
					return False
			else:
				return False
		else:
			return False









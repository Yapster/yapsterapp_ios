from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import datetime
from yap.models import *
from users.models import *

def check_session(user,session_id):
	try:
		session_verification = SessionVerification.objects.get(pk=session_id,is_active=True)
	except ObjectDoesNotExist:
		return ("There is no such session_id",False)
	check = session_verification.check_session(user=user,session_id=session_id)
	if isinstance(check,str):
		return (check,False)
	elif isinstance(check,bool):
		return (check,True)

def automatic_sign_in_check_session_id_and_device_token(user,session_id,session_device_token):
		try:
			session_verification = SessionVerification.objects.get(pk=session_id)
		except ObjectDoesNotExist:
			return("There is no such session_id.",False)
		check = session_verification.automatic_sign_in_check_session_id_and_device_token(user=user,session_device_token=session_device_token)
		if isinstance(check,str):
			return (check,False)
		elif isinstance(check,bool):
			return (check,True)

def sign_in_check_session_id_and_device_token(user,session_device_token):
	if SessionVerification.objects.filter(user=user,session_device_token=session_device_token,is_active=True).exists() == True:
		try:
			session_verification = SessionVerification.objects.get(user=user,session_device_token=session_device_token,is_active=True)
			check = session_verification.sign_in_check_session_id_and_device_token(session_device_token=session_device_token)
			if check == True:
				return (session_verification.pk,True)
		except MultipleObjectsReturned:
			active_sessions = SessionVerification.objects.filter(user=user,is_active=True)
			for active_session in active_sessions:
				active_session.close_session()
				session_verification = SessionVerification.objects.get_or_create(user=user,session_device_token=session_device_token,is_active=True)
				check = session_verification[0].sign_in_check_session_id_and_device_token(session_device_token=session_device_token)
				if check == True:
					return (session_verification[0].pk,True)
		if check == False:
			new_session_verification = SessionVerification.objects.create(user=user,session_device_token=session_device_token)
			return (new_session_verification.pk,True)
	elif SessionVerification.objects.filter(user=user,session_device_token=session_device_token,is_active=True).exists() == False:
		new_session_verification = SessionVerification.objects.create(user=user,session_device_token=session_device_token)
		return(new_session_verification.pk,True)

def trending_score(yap):
	yap_listen_count = yap.listens.count()
	yap_like_count = yap.likes.count()
	yap_reyap_count = yap.reyaps.count()
	yap_listen_score = yap_listen_count
	yap_like_score = yap_like_count * 2
	yap_reyap_score = yap_reyap_count * 4
	yap_trending_score = yap_listen_score + yap_like_score + yap_reyap_score
	return yap_trending_score


#When you're filtering and try to aggregate numbers and that we created fake likes, listens, reyaps.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from users.serializers import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.models import *
from datetime import datetime
from django.utils import timezone
from yapster_utils import check_session,automatic_sign_in_check_session_id_and_device_token,sign_in_check_session_id_and_device_token
from yap.serializers import *
from recommendating_users import recommended_users_to_follow_according_to_questionaire
from questionaire.models import *
import facebook as facebook
import twitter as twitter

@api_view(['PUT'])
def session_id(request):
	username = request.DATA['username']
	password = request.DATA['password']
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return Response({"message":"Invalid username","valid":False})
	if user.check_password(password):
		session_id = user.session.set_id()
		return Response({"message":"success","valid":True,"session_id":session_id})
	else:
		return Response({"Valid":False,"Message":"This is the incorrect password."})

class SignIn(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		option = request['option']
		option_type = request['option_type']
		password = request['password']
		try:
			if option_type == "email":
				user = User.objects.get(email=option)
			else:
				user = User.objects.get(username=option)
		except User.DoesNotExist:
			return Response({"valid":False,"message":"User does not exist"})
		if user.check_password(password) == True:
			if request.get('session_device_token'):
				session_device_token = request['session_device_token']
				check = sign_in_check_session_id_and_device_token(user=user,session_device_token=session_device_token)
				user.last_login = datetime.datetime.now()
				user.save(update_fields=['last_login'])
				if ForgotPasswordRequest.objects.filter(user=user,is_active=True).exists():
					forgot_password_request = ForgotPasswordRequest.objects.get(user=user,is_active=True,is_user_deleted=False)
					forgot_password_request.reset_password_security_code_not_used_and_user_signed_in()
				return Response({"user_id":user.pk,"valid":True,"session_id":check[0]})
			else:
				return Response({"valid":False,"message":"You must send a device token to sign in."})
		else:
			return Response({"user_id":user.pk,"valid":False,"message":"invalid password"})

class AutomaticSignIn(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = automatic_sign_in_check_session_id_and_device_token(user,request['session_id'],request['session_device_token'])
		if check[1]:
			return Response({"valid":True,"user_id":user.pk,"session_id":request['session_id']})
		else:
			return Response({"valid":False,"message":check[0]})


class SignOut(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request['session_id'])

		if check[1]:
			try: 
				session = SessionVerification.objects.get(pk=request['session_id'])
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"You haven't signed in and set your device token yet."})
			session.sign_out_device()
			return Response({"valid":True})
		else:
			return Response(check[0])

class SignUpVerifyEmail(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		email = kwargs.get('email')
		if User.objects.filter(email=email).exists() == True:
			return Response({"valid":False,"message":"This email already exists"})
		else:
			return Response({"valid":True,"message":"This email is available"})

class SignUpVerifyUsername(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		username = kwargs.get('username')
		if User.objects.filter(username=username).exists() == True:
			return Response({"valid":False,"message":"This username already exists"})
		else:
			return Response({"valid":True,"message":"This username is available"})

class SignUp(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		#kwargs = {str(k):str(v[0]) for k,v in dict(request.DATA).iteritems()}
		dob = datetime.datetime.strptime(kwargs['date_of_birth'],"%Y-%m-%d").date()
		age = (datetime.date.today() - dob).days/365.0
		if not age > 13 or not age < 120:
			return Response({"valid":False,"message":"Invalid age."})
		if kwargs.get('user_country_id'):
			try:
				user_country = Country.objects.get(pk=kwargs.pop('user_country_id'))
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"The country you have selected doesn't exist."})
			kwargs['user_country'] = user_country
		if kwargs.get('user_us_state_id') and user_country.country_name == "United States":
			try:
				user_us_state = USState.objects.get(pk=kwargs.pop('user_us_state_id'))
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"The US State you have selected doesn't exist."})
			kwargs['user_us_state'] = user_us_state
		if kwargs.get('user_us_zip_code'):
			try:
				user_us_zip_code = USZIPCode.objects.get(us_zip_code=kwargs.pop('user_us_zip_code'))
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"The ZIP Code you have selected doesn't exist."})
			kwargs['user_us_zip_code'] = user_us_zip_code
		if kwargs.get('user_city_name'):
			if user_country.country_name == "United States" and kwargs.get('user_us_state',None) and kwargs.get('user_us_zip_code',None):
				user_city = City.objects.get_or_create(city_name=kwargs.pop('user_city_name'),us_state=user_us_state,country=user_country,us_zip_code=user_us_zip_code)
			else:
				user_city = City.objects.get_or_create(city_name=kwargs.pop('user_city_name'),country=user_country)
			kwargs['user_city'] = user_city[0]
		if 'facebook_connection_flag' in kwargs:
			if kwargs.get('facebook_connection_flag') == True:
				if 'facebook_account_id' in kwargs:
					if 'facebook_access_token' in kwargs:
						facebook_access_token = kwargs.pop('facebook_access_token')
					else:
						return Response({"valid":False,"message":"You have connected your account with Facebook but not given a Facebook access token."})
				else:
					return Response({"valid":False,"message":"You have connected your account to Facebook but not given your Facebook account id."})
			else:
				pass
		if kwargs.get('twitter_shared_flag') == True:
				if kwargs.get('twitter_access_token_key'):
					if kwargs.get('twitter_access_token_secret'):
						if user.settings.twitter_connection_flag == True:
							twitter_access_token_key = kwargs.pop('twitter_access_token_key')
							twitter_access_token_secret = kwargs.pop('twitter_access_token_secret')
						else:
							return Response({"valid":False,"message":"User hasn't connected their account to Twitter."})
					else:
						return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_secret."})
				else:
					return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_key."})
		ids = UserFunctions.create(**kwargs)			
		if ids[0] == False:
			return Response({"valid":False,"message":ids[1]})
		else:
			template_html = 'welcome_new_user_email.html'
			template_text = 'welcome_new_user_email.txt'
			from_email = settings.DEFAULT_FROM_EMAIL
			subject = 'Welcome to Yapster!'
			html = get_template(template_html)
			text = get_template(template_text)
			user = User.objects.get(pk=ids[0])
			to = user.email
			d = Context({'user':user})
			text_content = text.render(d)
			html_content = html.render(d)
			msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			if 'facebook_connection_flag' in kwargs:
				if kwargs.get('facebook_connection_flag') == True:
					if 'facebook_account_id' in kwargs:
						if 'facebook_access_token' in kwargs:
							facebook_post = facebook.joined_post_on_facebook(user=user,facebook_access_token=facebook_access_token)
						else:
							return Response({"valid":False,"message":"You have connected your account with Facebook but not given a Facebook access token."})
					else:
						return Response({"valid":False,"message":"You have connected your account to Facebook but not given your Facebook account id."})
				else:
					pass
			if kwargs.get('twitter_shared_flag') == True:
				if kwargs.get('twitter_access_token_key'):
					if kwargs.get('twitter_access_token_secret'):
						if user.settings.twitter_connection_flag == True:
							twitter_post = twitter.joined_post_on_twitter(user=user,twitter_access_token_key=twitter_access_token_key,twitter_access_token_secret=twitter_access_token_secret)
						else:
							return Response({"valid":False,"message":"User hasn't connected their account to Twitter."})
					else:
						return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_secret."})
				else:
					return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_key."})
			return Response({"valid":True,"user_id":ids[0],"session_id":ids[4]})

class Recommendations(APIView):
	
	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if Answer.objects.filter(user=user,is_active=True).exists() == True:
				recommended_list = recommended_users_to_follow_according_to_questionaire(user=user)
				print "recommended_list", recommended_list
				print "questionaire has been compelted."
			else:
				recommended_list = Recommended.objects.filter(is_active=True)[:25]
				print "questionaire has not been answered."
			serialized = RecommendedSerializer(recommended_list,many=True)
			return Response(serialized.data)
		else:
			return Response(check[0])

class LoadSettings(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			settings = user.settings
			return Response(SettingsSerializer(settings).data)
		else:
			return Response(check[0])

class LoadProfile(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			settings = user.profile
			return Response(EditProfileInfoSerializer(settings).data)
		else:
			return Response(check[0])

class EditProfilePicture(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			info = UserInfo.objects.get(username=user.username)
			profile_picture_edited = info.edit_profile_picture(**request)
			return Response(profile_picture_edited)
		else:
			return Response(check[0])

class DeleteProfilePicture(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			info = UserInfo.objects.get(username=user.username)
			profile_picture_deleted = info.delete_profile_picture()
			return Response(profile_picture_deleted)
		else:
			return Response(check[0])

class EditProfile(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if kwargs.get('user_country_id'):
				try:
					user_country = Country.objects.get(pk=kwargs.pop('user_country_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The country you have selected doesn't exist."})
				kwargs['user_country'] = user_country
			if kwargs.get('user_us_state_id') and user_country.country_name == "United States":
				try:
					user_us_state = USState.objects.get(pk=kwargs.pop('user_us_state_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The US State you have selected doesn't exist."})
				kwargs['user_us_state'] = user_us_state
			if kwargs.get('user_us_zip_code'):
				try:
					user_us_zip_code = USZIPCode.objects.get(us_zip_code=kwargs.pop('user_us_zip_code'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The ZIP Code you have selected doesn't exist."})
				kwargs['user_us_zip_code'] = user_us_zip_code
			if kwargs.get('user_city_name') or kwargs.get('user_city_name') == '':
				if user_country.country_name == "United States" and kwargs.get('user_us_state',None) and kwargs.get('user_us_zip_code',None):
					user_city = City.objects.get_or_create(city_name=kwargs.pop('user_city_name'),us_state=user_us_state,country=user_country,us_zip_code=user_us_zip_code,is_active=True)
				else:
					user_city = City.objects.get_or_create(city_name=kwargs.pop('user_city_name'),country=user_country,is_active=True)
				kwargs['user_city'] = user_city[0]
			info1 = UserInfo.objects.get(username=user.username)
			info2 = info1.modify_account(**kwargs)
			if isinstance(info2,str):
				return Response({"valid":False,"message":info2})
			else:
				return Response({"valid":True,"message":"Your profile has successfully been edited."})
		else:
			return Response(check[0])

class EditSettings(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if kwargs.get('user_country_id'):
				try:
					user_country = Country.objects.get(pk=kwargs.pop('user_country_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The country you have selected doesn't exist."})
				kwargs['user_country'] = user_country
			if kwargs.get('user_us_state_id') and user_country.country_name == "United States":
				try:
					user_us_state = USState.objects.get(pk=kwargs.pop('user_us_state_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The US State you have selected doesn't exist."})
				kwargs['user_us_state'] = user_us_state
			if kwargs.get('user_us_zip_code'):
				try:
					user_us_zip_code = USZIPCode.objects.get(us_zip_code=kwargs.pop('user_us_zip_code'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The ZIP Code you have selected doesn't exist."})
				kwargs['user_us_zip_code'] = user_us_zip_code
			if kwargs.get('user_city_name'):
				if user_country.country_name == "United States" and kwargs.get('user_us_state',None) and kwargs.get('user_us_zip_code',None):
					user_city = City.objects.get_or_create(city_name=kwargs.pop('user_city_name'),us_state=user_us_state,country=user_country,us_zip_code=user_us_zip_code)
				else:
					user_city = City.objects.get_or_create(city_name=kwargs.pop('user_city_name'),country=user_country)
				kwargs['user_city'] = user_city[0]
			info1 = UserInfo.objects.get(username=user.username)
			info2 = info1.modify_account(**kwargs)
			new_settings = user.settings
			serialized = SettingsSerializer(new_settings,data=self.request.DATA)
			return Response(serialized.data)
		else:
			return Response(check[0])

class DisconnectFacebookAccount(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if 'facebook_connection_flag' in kwargs:
				if kwargs.get('facebook_connection_flag') == False:
					facebook_changes = {}
					facebook_changes['facebook_connection_flag'] = False
					facebook_changes['facebook_account_id'] = None
					facebook_changes['facebook_page_connection_flag'] = False
					facebook_changes['facebook_page_id'] = None
					facebook_changes['facebook_share_reyap'] = False
					info1 = UserInfo.objects.get(username=user.username)
					info2 = info1.modify_account(**facebook_changes)
					new_settings = user.settings
					serialized = SettingsSerializer(new_settings,data=self.request.DATA)
					return Response(serialized.data)
				else:
					return Response({"valid":False,"message":"The facebook_connection_flag must be false to disconnect the Facebook Account."})
			else:
				return Response({"valid":False,"message":"There must be a facebook_connection_flag sent which must be false to disconnect the Facebook Account."})
		else:
			return Response(check[0])

class DisconnectTwitterAccount(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if 'twitter_connection_flag' in kwargs:
				if kwargs.get('twitter_connection_flag') == False:
					twitter_changes = {}
					twitter_changes['twitter_connection_flag'] = False
					twitter_changes['twitter_account_id'] = None
					twitter_changes['twitter_share_reyap'] = False
					info1 = UserInfo.objects.get(username=user.username)
					info2 = info1.modify_account(**twitter_changes)
					new_settings = user.settings
					serialized = SettingsSerializer(new_settings,data=self.request.DATA)
					return Response(serialized.data)
				else:
					return Response({"valid":False,"message":"The twitter_connection_flag must be false to disconnect the Twitter Account."})
			else:
				return Response({"valid":False,"message":"There must be a twitter_connection_flag sent which must be false to disconnect the Twitter Account."})
		else:
			return Response(check[0])

class ProfileInfo(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		print request
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			profile_user = User.objects.get(pk=request['profile_user_id'])
			profile = profile_user.profile
			serialized = ProfileInfoSerializer(profile,data=self.request.DATA,context={'user':user})
			return Response(serialized.data)
		else:
			return Response(check[0])

class ProfileStreams(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		a = timezone.now()
		user = User.objects.get(pk=request['user_id'])
		if request['profile_user_id']:
			profile_user = User.objects.get(pk=request['profile_user_id'])
		else:
			profile_user = user
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			after_yap = request.get("after_yap",None)
			after_reyap = request.get("after_reyap",None)
			after = request.get("after",None)
			stream_type = request['stream_type']
			if stream_type == "posts":
				stream = profile_user.functions.load_profile_posts(request['amount'],after_yap=after_yap,after_reyap=after_reyap)
				serialized = ProfilePostStreamSerializer(stream,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
			elif stream_type == "likes":
				stream = profile_user.functions.load_profile_likes(request['amount'],after=after)
				serialized = ProfileLikeStreamSerializer(stream,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
			elif stream_type == "listens":
				if profile_user.profile.listen_stream_public == True or user == profile_user:
					stream = profile_user.functions.load_profile_listens(request['amount'],after=after)
					serialized = ProfileListenStreamSerializer(stream,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
				else:
					return Response({"Valid":False, "Message":"This user's listen stream is private."})
			else:
				stream = Yap.objects.none()
		else:
			return Response(check[0])

class ListOfFollowers(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		profile_user = User.objects.get(pk=request['profile_user_id'])
		if check[1]:
			if 'after' in request:
				list_of_followers = profile_user.functions.list_of_followers(queryset=True,amount=request['amount'],after=request['after'])
			else:
				list_of_followers = profile_user.functions.list_of_followers(queryset=True,amount=request['amount'])
			serialized = ListOfFollowersSerializer(list_of_followers,data=self.request.DATA,many=True,context={'profile_user':profile_user})
			return Response(serialized.data)
		else:
			return Response(check[0])

class ListOfFollowing(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		profile_user = User.objects.get(pk=request['profile_user_id'])
		if check[1]:
			if 'after' in request:
				list_of_following = profile_user.functions.list_of_following(queryset=True,amount=request['amount'],after=request['after'])
			else:
				list_of_following = profile_user.functions.list_of_following(queryset=True,amount=request['amount'])
			serialized = ListOfFollowingSerializer(list_of_following,data=self.request.DATA,many=True,context={'profile_user':profile_user})
			return Response(serialized.data)
		else:
			return Response({"Valid":False,"Message":check[0]})

class ForgotPasswordRequestForEmail(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		if User.objects.filter(is_active=True,email=request['email']).exists():
			user = User.objects.get(is_active=True,email=request['email'])
			forgot_password_request = ForgotPasswordRequest.objects.get_or_create(is_active=True,user=user,user_email=user.email)
			forgot_password_request = forgot_password_request[0]
			return Response({"valid":True,"message":"Please check your email for your security code to reset your password."})
		else:
			return Response({"valid":False,"message":"There is no active user with this email."})

class ResetPasswordRequest(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		option = request['option']
		option_type = request['option_type']
		try:
			if option_type == "email":
				user = User.objects.get(email=option)
			else:
				user = User.objects.get(username=option)
		except User.DoesNotExist:
			return Response({"valid":False,"message":"User does not exist"})
		if ForgotPasswordRequest.objects.filter(is_active=True,user=user,user_email=user.email).exists():
			forgot_password_request = ForgotPasswordRequest.objects.get(is_active=True,user=user,user_email=user.email)
			if forgot_password_request.reset_password_security_code == request['reset_password_security_code']:
				forgot_password_request.reset_password_security_code_used()
				user.set_password(request['new_password'])
				user.save(update_fields=['password'])
				return Response({"valid":True,"message":"Your password has been successfully changed."})
			else:
				return Response({"valid":False,"message":"The security code doesn't match what was sent to your email."})
		else:
			return Response({"valid":False,"message":"You have not requested for a security code. Please click the forgot password button on the sign up screen and request for a security code."})









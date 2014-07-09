import requests
from bs4 import BeautifulSoup as BS
import datetime
import webbrowser
from users.models import *
from django.contrib.auth.models import User
from yap.models import Yap

class APIRequest:
	def __init__(self, host='http://127.0.0.1:8000/api/0.0.1/', extension=None):
		if extension:
			if not extension.endswith("/"):
				extension += "/"
			self.host = host + extension
			print host
		else:
			self.host = host
			print host
	def call(self,extension,request_type,data=None):
		print data
		url = self.host + extension
		print url
		print 1
		if request_type == "get":
			r = requests.get(url,data=data)
			print 2
		elif request_type == "post":
			r = requests.post(url,data=data)
			print 3
		if request_type == "put":
			r = requests.put(url,data=data)
			print 3.3
		elif request_type == "delete":
			r = requests.delete(url,data=data)
			print 3.6
		try:
			response = r.json()
			print 4
			return response
		except:
			print 5
			self.display_error(r.text,exception=True)
	def display_error(self,text,exception=False):
		soup = BS(text)
		summary = soup.find("div", { "id" : "summary" }) 
		message = "\n\n" + summary.h1.text + "\n\n" + summary.pre.text + "\n"
		#with open('error.html','w') as f:
			#f.write(text)
		#webbrowser.open('file:///Users/Gurkaran/Documents/error.html')
		if exception:
			raise BaseException(message)
			print text
		else:
			print message

class APIYapRequest(APIRequest):
	def create(self,user,audio_path,length,title, session_id, hashtags=None, user_tags_flag=False, user_tags=None):
		d = locals()
		del d['self']
		ext = "create/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APIActionRequest(APIRequest):
	def listen_to(self,user,user_requested,session_id):
		d = locals()
		del d['self']
		ext = "listentouser/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response
	def like(self,user,obj_type,obj,session_id):
		d = locals()
		del d['self']
		ext = "like/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response
	def reyap(self,user,obj_type,obj,session_id):
		d = locals()
		del d['self']
		ext = "reyap/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response
	def listen(self,user,obj_type,obj,session_id):
		d = locals()
		del d['self']
		ext = "listen/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APIUserRequest(APIRequest):
	def set_id(self,username,password):
		d = locals()
		del d['self']
		ext = "setsession/"
		request_type = "put"
		response = self.call(ext,request_type,data=d)
		return response
	def settings(self,user_id,session_id,request_type):
		d = locals()
		del d['self'],d['request_type']
		for key,value in d.iteritems():
			if isinstance(value,dict):
				print key
				del d[key]
				for new_key,new_value in value.iteritems():
					d[new_key] = new_value
			else:
				print type(value)
		print d
		ext = "settings/"
		response = self.call(ext,request_type,data=d)
		return response
	def recommended(self,user_id,session_id):
		d = locals()
		del d['self']
		ext = "recommended/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response
	def sign_up(self,username,email,password,first_name,last_name,date_of_birth):
		d = locals()
		del d['self']
		ext = "signup/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response
	def sign_in(self,option,option_type,password):
		d = locals()
		del d['self']
		ext = "signin/"
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response
	def profile_info(self,user_id,viewer,session_id):
		d = locals()
		del d['self']
		ext = 'profile/info/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response
	def profile_streams(self,user_id,viewer,stream_type,amount,session_id,after=None):
		d = locals()
		del d['self']
		ext = 'profile/stream/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APIStreamRequest(APIRequest):
	def load(self,user_id,amount,session_id,after=None):
		d = locals()
		del d['self']
		print d
		ext = 'stream/load/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APIAllNotificationsRequest(APIRequest):
	def load(self,user_id,amount,session_id,after=None):
		d = locals()
		del d['self']
		ext = 'notifications/load/all/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APIUnreadNotificationsRequest(APIRequest):
	def load(self,user_id,amount,session_id,after=None):
		d = locals()
		del d['self']
		ext = 'notifications/load/unread/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APILoadExploreChannelsRequest(APIRequest):
	def load(self,user_id,session_id):
		d = locals()
		del d['self']
		ext = 'yap/explore/channels/load/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APILoadYapChannelsRequest(APIRequest):
	def load(self,user_id,session_id):
		d = locals()
		del d['self']
		ext = 'yap/channels/load/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

class APIRecommendUserRequest(APIRequest):
	def recommend(self,user_id,session_id,date_will_deactive):
		d = locals()
		del d['self']
		ext = 'users/recommend/'
		request_type = "post"
		response = self.call(ext,request_type,data=d)
		return response

users = APIUserRequest(extension="users/")
print dir(users)
yaps = APIYapRequest(extension="yap/")
actions = APIActionRequest(extension="actions/")
streams = APIStreamRequest(extension="stream/")

#print yaps.create([1],"some_path/1",20,"title")
"""
a = users.sign_up("ryan","ryan@yapsterapp.com","password","ryan","saxe",datetime.date(1995,7,16))
b = users.sign_up("math","math@yapsterapp.com","password","math","math",datetime.date(1991,11,24))
c = users.sign_up("test","test@yapsterapp.com","password","test","test",datetime.date(1972,1,18))
d = users.sign_up("guest","guest@yapsterapp.com","password","guest","guest",datetime.date(1980,4,1))
e = users.sign_up("abc","abc@yapsterapp.com","password","abc","123",datetime.date(1988,9,6))
f = users.sign_up("hello","hello@yapsterapp.com","password","hello","world",datetime.date(2005,3,23))

print a
print b
print c
print d
print e
print f

print actions.listen_to(a['user_id'],b['user_id'])
print actions.listen_to(a['user_id'],c['user_id'])
print actions.listen_to(a['user_id'],d['user_id'])
print actions.listen_to(a['user_id'],e['user_id'])

print actions.listen_to(b['user_id'],a['user_id'])
print actions.listen_to(b['user_id'],c['user_id'])
print actions.listen_to(b['user_id'],d['user_id'])

print actions.listen_to(c['user_id'],a['user_id'])
print actions.listen_to(c['user_id'],b['user_id'])

print actions.listen_to(d['user_id'],a['user_id'])
print actions.listen_to(d['user_id'],c['user_id'])
print actions.listen_to(d['user_id'],e['user_id'])

print actions.listen_to(e['user_id'],a['user_id'])
print actions.listen_to(e['user_id'],d['user_id'])
django_users = User.objects.all()

#a = users.sign_in("ryan","username","password)
if Yap.objects.all().count() > 0:
	django_yap_num = Yap.objects.last().pk
else:
	django_yap_num = 0

yaps.create(django_users[0].pk,"path/" + str(django_yap_num + 1),14,"my title")
yaps.create(django_users[0].pk,"path/" + str(django_yap_num + 2),26,"blah blah")
yaps.create(django_users[0].pk,"path/" + str(django_yap_num + 3),27,"something")
yaps.create(django_users[0].pk,"path/" + str(django_yap_num + 4),7,"thoughts")
yaps.create(django_users[0].pk,"path/" + str(django_yap_num + 5),11,"guess that sound")
yaps.create(django_users[1].pk,"path/" + str(django_yap_num + 6),12,"hello world")
yaps.create(django_users[2].pk,"path/" + str(django_yap_num + 7),18,"emordnilap")
yaps.create(django_users[3].pk,"path/" + str(django_yap_num + 8),9,"title")
yaps.create(django_users[4].pk,"path/" + str(django_yap_num + 9),21,"abcdefg")
"""

#print streams.load(django_users[0].pk,1,django_users[0].session.session_id)
'''
user = django_users[10]
yaps = [y.pk for y in Yap.objects.exclude(user=user)]
print user.session.session_id
from yapster_utils import check_session
print user.session.check(user.session.session_id)
print check_session(user,user.session.session_id)
trial = users.settings(user.pk,user.session.session_id,"put",notify_for_likes=False)
if trial == [{u'message': u'please send username and password. session_id is not up to date', u'valid': True}, False]:
	users.set_id(user.username,"password_of_" + user.username)
	print users.settings(user.pk,user.session.session_id,"put",notify_for_likes=False)
else:
	print trial
print user.settings.notify_for_mentions
print UserInfo.objects.get(username=user.username).notify_for_mentions

#print actions.reyap(user.pk,"yap",yaps[5],user.session.session_id)

notificationsList = APINotificationsRequest()
user = User.objects.get(pk=8)
print notificationsList.load(user.pk,20,user.session.session_id)
'''
#Stream Test
'''
streamList = APIStreamRequest()
user = User.objects.get(pk=20)
print streamList.load(user_id=user.pk,amount=5,session_id=27,after=748)
#'''
#Sign In Test
'''
gurkaranSignIn = APIUserRequest(extension='users/')
gurkaranSignIn.sign_in('karl_hagy','username','karl_hagy')
#'''
#Load All Notifications 
'''
gurkaranNotification = APIAllNotificationsRequest()
user = User.objects.get(pk=20)
print gurkaranNotification.load(user_id=user.pk,amount=3,session_id=26,after=234)
#'''
#Load Unread Notifications 
'''
gurkaranNotification = APIUnreadNotificationsRequest()
user = User.objects.get(pk=20)
print gurkaranNotification.load(user_id=user.pk,amount=3,session_id=26)
#'''
#Yap Test
'''
gurkaranYap = APIYapRequest(extension='yap/')
user = User.objects.get(pk=8)
audio_path = 'yapster/users/8/yaps/100000/audio/1'
length = '20'
title = 'Testing 123 Anyone Listening?'
session_id = '28'
hashtags = ["coolstory", "getitgirl"]
#user_tags = ["Lovetta_Kernes"]
user_tags_flag = 'False'
print gurkaranYap.create(user=user.pk, audio_path=audio_path, length=length, title=title, session_id=session_id, hashtags=hashtags, user_tags_flag=user_tags_flag)
'''
#Test Delete Notifications
'''
#Like Test
gurkaranLike = APIActionRequest(extension='actions/')
user = User.objects.get(pk=8)
obj_type = 'yap'
obj = 183
session_id = 28
print gurkaranLike.like(user=user.pk, obj_type=obj_type, obj=obj, session_id=session_id)
'''
#Sign Up Test
'''
gurkaranSignUp = APIUserRequest(extension='users/')
gurkaranSignUp.sign_up('yapster123','yapster123@yapsterapp.com','abc123','Yap','Ster','1993-05-14')
#username,email,password,first_name,last_name,date_of_birth
#'''
#Recommended Test
'''
gurkaranRecommended = APIUserRequest(extension='users/')
user = User.objects.get(pk=8)
gurkaranRecommended.recommended('28','31')
'''
#Profile Info
'''
gurkaranProfileDetails = APIUserRequest(extension='users/')
user = User.objects.get(pk=20)
gurkaranProfileDetails.profile_info(user_id=20,viewer=20,session_id=27)

#def profile_info(self,user_id,viewer,session_id):
'''
#Profile Streams
'''
gurkaranProfileStreams = APIUserRequest(extension='users/')
user = User.objects.get(pk=20)
gurkaranProfileStreams.profile_streams(user_id=20,viewer=20,session_id=27,stream_type="post",amount=5)
#def profile_streams(self,user_id,viewer,stream_type,amount,session_id,after=None):
'''
#Settings
'''
gurkaranSettingsLoad = APIUserRequest(extension='users/')
user = user.objects.get(pk=20)
gurkaranSettingsLoad.settings(user_id=20,session_id=27,request_type='post')
#def settings(self,user_id,session_id,request_type,**kwargs):
'''
#LoadExploreChannels
'''
gurkaranLoadsExploreChannels = APILoadExploreChannelsRequest()
user = user.objects.get(pk=20)
gurkaranLoadsExploreChannels.load(user_id=20,session_id=27)
'''
#LoadExploreChannels
'''
gurkaranLoadsExploreChannels = APILoadExploreChannelsRequest()
user = user.objects.get(pk=20)
gurkaranLoadsExploreChannels.load(user_id=20,session_id=27)
'''
#LoadYapChannels
'''
gurkaranLoadsYapChannels = APILoadYapChannelsRequest()
user = user.objects.get(pk=20)
gurkaranLoadsYapChannels.load(user_id=20,session_id=28)
'''
#RecommendUser
#'''
gurkaranRecommendsUsers = APIRecommendUserRequest()
user = User.objects.get(pk=20)
gurkaranRecommendsUsers.recommend(user_id=20,session_id=28,date_will_deactive='2014-04-24')




import django_facebook
from aws import *
import datetime
from django.conf import settings
from open_facebook import OpenFacebook

def share_yap_on_facebook(user,facebook_access_token,yap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		name = str(yap.user.first_name) + ' ' + str(yap.user.last_name) + " (@" + str(user.username) + ") posted a yap on Yapster"
		api_url = str(user.settings.facebook_account_id) + '/feed'
		url = "http://web.yapster.co/yap/" + str(yap.pk)
		b = connect_s3(bucket_name="yapsterapp")
		if yap.picture_flag == True:
			yap_picture_key = b.get_key(yap.picture_cropped_path)
			yap_picture_url = yap_picture_key.generate_url(expires_in=600)
		elif yap.picture_flag == False:
			yap_picture_key = b.get_key(user.profile.profile_picture_path)
			yap_picture_url = yap_picture_key.generate_url(expires_in=600)
		if yap.description != None:
			fb_share_yap_message = "\"" + str(yap.title) + "\" - " + str(yap.description) + " " + "\n" + str(url)
		elif yap.description == None:
			fb_share_yap_message = "\"" + str(yap.title) + "\" " + str(url)
		fb_share_yap_description = "Listen to this yap - and other yaps from " + str(user.first_name) + " " + str(user.last_name) 
		fb_share_yap = facebook.set(api_url, link=url, picture=yap_picture_url, name=name, description=fb_share_yap_description,message=fb_share_yap_message)['id']
		return fb_share_yap
	else:
		return "User has not set up a facebook_account_id."

def share_yap_story_on_facebook(user,facebook_access_token,yap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		name = str(yap.title)
		object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yapped'
		print object_api_url
		url = "http://web.yapster.co/yap/" + str(yap.pk) + '/'
		b = connect_s3(bucket_name="yapsterapp")
		if yap.picture_flag == True:
			yap_picture_key = b.get_key(yap.picture_cropped_path)
			yap_picture_url = yap_picture_key.generate_url(expires_in=600)
		elif yap.picture_flag == False:
			yap_picture_key = b.get_key(user.profile.profile_picture_path)
			yap_picture_url = yap_picture_key.generate_url(expires_in=600)
		if yap.description != None:
			yap = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":name,"description":yap.description})['id']
		elif yap.description == None:
			yap = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":name})['id']
		story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:yap'
		fb_share_yap = facebook.set(story_api_url,yap=yap)['id']
		return fb_share_yap
	else:
		return "User has not set up a facebook_account_id."

def share_reyap_on_facebook(user,facebook_access_token,reyap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		name = str(user.first_name) + ' ' + str(user.last_name) + " (@" + str(user.username) + ") reyapped a yap on Yapster"
		api_url = str(user.settings.facebook_account_id) + '/feed'
		url = "http://web.yapster.co/reyap/" + str(reyap.pk)
		b = connect_s3(bucket_name="yapsterapp")
		if reyap.yap.picture_flag == True:
			reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		elif reyap.yap.picture_flag == False:
			reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		if reyap.yap.description != None:
			fb_share_reyap_message = "\"" + str(yap.title) + "\" - " + str(yap.description) + " " + "\n" + str(url)
		elif reyap.yap.description == None:
			fb_share_reyap_message = "\"" + str(yap.title) + "\" " + str(url)
		fb_share_reyap_description = "Listen to this reyap - and other reyaps/yaps from " + str(reyap.user.first_name) + " " + str(reyap.user.last_name) 
		fb_share_reyap = facebook.set(api_url, link=url, picture=reyap_picture_url, name=name, description=fb_share_reyap_description,message=fb_share_reyap_message)['id']
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."

def share_reyap_story_on_facebook(user,facebook_access_token,reyap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:reyapped'
		name = str(reyap.yap.title)
		url = "http://web.yapster.co/reyap/" + str(reyap.pk) + '/'
		b = connect_s3(bucket_name="yapsterapp")
		if reyap.yap.picture_flag == True:
			reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		elif reyap.yap.picture_flag == False:
			reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		if reyap.reyap_flag == True:
			object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:reyap'
			if reyap.yap.description != None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name,"description":reyap.yap.description})['id']
			elif reyap.yap.description == None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name})['id']
			fb_share_reyap = facebook.set(story_api_url,reyap=object_reyapped)['id']
		elif reyap.reyap_flag == False:
			object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yap'
			if reyap.yap.description != None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name,"description":reyap.yap.description})['id']
			elif reyap.yap.description == None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name})['id']
			fb_share_reyap = facebook.set(story_api_url,yap=object_reyapped)['id']
		print object_api_url
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."

def share_like_story_on_facebook(user,facebook_access_token,yap=None,reyap=None):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:liked'
		if yap != None and reyap == None:
			name = str(yap.title)
			url = "http://web.yapster.co/yap/" + str(yap.pk) + '/'
			b = connect_s3(bucket_name="yapsterapp")
			if yap.picture_flag == True:
				yap_picture_key = b.get_key(yap.picture_cropped_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			elif yap.picture_flag == False:
				yap_picture_key = b.get_key(user.profile.profile_picture_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yap'
			if yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":name,"description":yap.description})['id']
			elif yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":name})['id']
			print object_api_url
			print object_liked
			print story_api_url
			fb_share_reyap = facebook.set(story_api_url,yap=object_liked)['id']
		elif yap == None and reyap != None:
			name = str(reyap.yap.title)
			url = "http://web.yapster.co/reyap/" + str(reyap.pk) + '/'
			b = connect_s3(bucket_name="yapsterapp")
			if reyap.yap.picture_flag == True:
				reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			elif reyap.yap.picture_flag == False:
				reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:reyap'
			if reyap.yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name,"description":reyap.yap.description})['id']
			elif reyap.yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name})['id']
			print object_api_url
			print object_liked
			print story_api_url
			fb_share_reyap = facebook.set(story_api_url,reyap=object_liked)['id']
		print object_api_url
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."

def share_listen_story_on_facebook(user,facebook_access_token,yap=None,reyap=None):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:listened_to'
		if yap != None and reyap == None:
			name = str(yap.title)
			url = "http://web.yapster.co/yap/" + str(yap.pk)
			b = connect_s3(bucket_name="yapsterapp")
			if yap.picture_flag == True:
				yap_picture_key = b.get_key(yap.picture_cropped_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			elif yap.picture_flag == False:
				yap_picture_key = b.get_key(user.profile.profile_picture_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yap'
			if yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":name,"description":yap.description})['id']
			elif yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":name})['id']
			print object_api_url
			print object_liked
			print story_api_url
			fb_share_reyap = facebook.set(story_api_url,yap=object_liked)['id']
		elif yap == None and reyap != None:
			name = str(reyap.yap.title)
			url = "http://web.yapster.co/reyap/" + str(reyap.pk) + '/'
			b = connect_s3(bucket_name="yapsterapp")
			if reyap.yap.picture_flag == True:
				reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			elif reyap.yap.picture_flag == False:
				reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:reyap'
			if reyap.yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name,"description":reyap.yap.description})['id']
			elif reyap.yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":name})['id']
			print object_api_url
			print object_liked
			print story_api_url
			fb_share_reyap = facebook.set(story_api_url,reyap=object_liked)['id']
		print object_api_url
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."
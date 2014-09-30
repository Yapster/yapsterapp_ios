from TwitterAPI import TwitterAPI
from django.conf import settings
from aws import *
import StringIO
import datetime
import json

def share_yap_on_twitter(user,yap,twitter_access_token_key,twitter_access_token_secret):
	twitter = TwitterAPI(consumer_key=settings.TWITTER_CONSUMER_KEY,consumer_secret=settings.TWITTER_CONSUMER_SECRET,access_token_key=twitter_access_token_key,access_token_secret=twitter_access_token_secret)
	length_of_status = len(yap.title) + len(yap.user.username)
	if yap.picture_flag == True:
		status = "@" + str(yap.user.username) + " yapped \"" + str(title) + '\" -  web.yapster.co/yap/' + str(yap.pk)
		if length_of_title_and_username >  64:
			extra_length_of_title = length_of_title - 65
			title = yap.title[:(-extra_length_of_title -3)].upper() + "..." # -3 for three dots ...
		elif length_of_title <= 65:
			title = yap.title
		b = connect_s3(bucket_name="yapsterapp")
		yap_picture_key = b.get_key(yap.picture_path)
		fp = StringIO.StringIO()
		yap_picture_key.get_file(fp)
		yap_picture = fp.getvalue()
	elif yap.picture_flag == False:
		if length_of_title >  87:
			extra_length_of_title = length_of_title - 88
			title = yap.title.replace[:-extra_length_of_title].upper()
		elif length_of_title <= 88:
			title = yap.title
		status = str(title) + ' -  web.yapster.co/yap/' + str(yap.pk)
	length_of_status = len(status)
	if length_of_status > 140:
		return "This status is too long for Twitter."
	elif length_of_status <= 140:
		r =twitter.request('statuses/update_with_media',{'status':status}, {'media[]': yap_picture})
		#print("Success" if r.status_code == 200 else 'Failure')
		return json.loads(r.text)['id']

def share_reyap_on_twitter(user,yap,twitter_access_token_key,twitter_access_token_secret):
	twitter = TwitterAPI(consumer_key=settings.TWITTER_CONSUMER_KEY,consumer_secret=settings.TWITTER_CONSUMER_SECRET,access_token_key=twitter_access_token_key,access_token_secret=twitter_access_token_secret)
	length_of_title_and_username = len(yap.title) + len(yap.user.username)
	if yap.picture_flag == True:
		if length_of_title_and_username >  64:
			extra_length_of_title = length_of_title - 65
			title = yap.title[:(-extra_length_of_title -3)].upper() + "..." # -3 for three dots ...
		elif length_of_title <= 65:
			title = yap.title
		status = "@" + str(yap.user.username) + " yapped \"" + str(title) + '\" -  web.yapster.co/yap/' + str(yap.pk) 
		b = connect_s3(bucket_name="yapsterapp")
		yap_picture_key = b.get_key(yap.picture_path)
		fp = StringIO.StringIO()
		yap_picture_key.get_file(fp)
		yap_picture = fp.getvalue()
	elif yap.picture_flag == False:
		if length_of_title >  87:
			extra_length_of_title = length_of_title - 88
			title = yap.title.replace[:-extra_length_of_title].upper()
		elif length_of_title <= 88:
			title = yap.title
		status = str(title) + ' -  web.yapster.co/yap/' + str(yap.pk)
	length_of_status = len(status)
	if length_of_status > 140:
		return "This status is too long for Twitter."
	elif length_of_status <= 140:
		r =twitter.request('statuses/update_with_media',{'status':status}, {'media[]': yap_picture})
		#print("Success" if r.status_code == 200 else 'Failure')
		return json.loads(r.text)['id']
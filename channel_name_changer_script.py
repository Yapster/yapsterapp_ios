from yap.models import *
from users.models import *
from notification.models import *
from notification.serializers import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from apns import APNs, Frame, Payload
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import time
import random
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

'''
def change_channels_paths():
	
	channels = Channel.objects.all()
	for channel in channels:
		print channel.channel_name
		channel.icon_explore_path_clicked='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_clicked.png'
		channel.icon_explore_path_unclicked ='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_unclicked.png'
		channel.icon_yap_path_clicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_clicked.png'
		channel.icon_yap_path_unclicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_unclicked.png'
		channel.save(update_fields=['icon_explore_path_clicked','icon_explore_path_unclicked','icon_yap_path_clicked','icon_yap_path_unclicked'])

#change_channels_paths()

def change_channels_path():
	
	channels = Channel.objects.all()
	for channel in channels:
		print channel.channel_name
		channel.icon_explore_path_clicked='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_clicked.png'
		channel.icon_explore_path_unclicked ='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_unclicked.png'
		channel.icon_yap_path_clicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_clicked.png'
		channel.icon_yap_path_unclicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_unclicked.png'
		channel.save(update_fields=['icon_explore_path_clicked','icon_explore_path_unclicked','icon_yap_path_clicked','icon_yap_path_unclicked'])

#change_channels_path()

def delete_channels():

	channels = Channel.objects.all()
	for channel in channels: 
		print channel.channel_name
		channel.delete()

#delete_channels()

channels = [
'Art',
'Beauty',
'Business',
'Celebrity Gossip',
'Comedy',
'Education',
'Family',
'Fashion',
'Finance',
'Food and Drinks',
'Health and Fitness',
'Misc',
'Movies',
'Music',
'News',
'Night Life',
'Organizations',
'Politics',
'Religion',
'Sports',
'Summer',
'Technology',
'TV',

]

def create_channels():

print("starting channels")
#''
total = len(channels)
print total
for i,channel in enumerate(channels):
	channel_string = channel.replace(" ","")
	print(channel + " " + str(i) + "/" + str(total))
	Channel.objects.create(channel_name=channel,
		channel_description=channel,
		icon_explore_path_clicked='yapsterchannels/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_clicked.png',
		icon_explore_path_unclicked ='yapsterchannels/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_unclicked.png',
		icon_yap_path_clicked='yapsterchannels/' + str(channel_string.lower()) + '/yap/' + str(channel_string.lower()) + '_yap_clicked.png',
		icon_yap_path_unclicked='yapsterchannels/' + str(channel_string.lower()) + '/yap/' + str(channel_string.lower()) + '_yap_unclicked.png')


#create_channels()


def recalculate_yap_count():

	users = User.objects.all()
	for user in users:
		print user
		total_number_of_yaps_for_this_user = len(Yap.objects.filter(user=user,is_active=True))
		user.profile.yap_count = total_number_of_yaps_for_this_user
		user.profile.save(update_fields=['yap_count'])

recalculate_yap_count()


def delete_useless_users():
	users = User.objects.filter(pk__gte=31)
	for user in users:
		print user
		users_listens = user.listens.all()
		for listen in users_listens:
			print listen.pk
			listen.delete()
		users_likes = user.likes.all()
		for like in users_likes:
			print like.pk
			like.delete()
		users_reyaps = user.reyaps.all()
		for reyap in users_reyaps:
			print reyap.pk
			reyap.delete()
		users_yaps = user.yaps.all()
		for yap in users_yaps:
			print yap.pk
			yap.delete()
		users_notifications = user.notifications.all()
		for notification in users_notifications:
			notification.delete()
		user.delete()

delete_useless_users()
#'''
'''
def change_all_users_to_listen_stream_public():
	users = User.objects.all()
	for user in users:
		print user
		user_info = UserInfo.objects.get(pk=user.pk)
		user_info.modify_account(listen_stream_public=True)

change_all_users_to_listen_stream_public()
#'''

def testing_123_push_notification():
	print 1
	user = User.objects.get(pk=26)
	apns = APNs(use_sandbox=True,cert_file='yapster_ios_push_cert_dev.pem',key_file='yapster_ios_push_key_dev.pem')
	#Send a notification
	notification1 = []
	number = 100
	'''
	notification = Notification.objects.filter(pk=number)
	for notification_ in notification:
		notification_type = notification_.notification_type.notification_name
		notification_user = notification_.user.pk
		notification_user_requested = notification_.acting_user.pk
		#notification_json = json.dumps(list(notification_type), cls=DjangoJSONEncoder)
	'''
	token_hex1 = user.session.session_udid
	print token_hex1
	token_hex2 = token_hex1.replace('<','')
	token_hex3 = token_hex2.replace('>','')
	token_hex = token_hex3.replace(' ','')
	print token_hex
	alert = "You're not working yet!"
	payload = Payload(alert=alert,sound="default",badge=1)
	apns.gateway_server.send_notification(token_hex,payload)
	print payload
	print user.pk
	print ("success")
testing_123_push_notification()

def investor_email():
	template_html = 'investor_update_email.html'
	template_text = 'investor_update_email.txt'
	from_email = settings.DEFAULT_FROM_EMAIL
	subject = 'Investor Update for Week of 7/14/14 - Yapster,Inc.'
	html = get_template(template_html)
	text = get_template(template_text)
	to = 'jb3991@nyu.edu'
	name = 'Mr. Jonathan Bach'
	d = Context({'name':name})
	text_content = text.render(d)
	html_content = html.render(d)
	msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

#investor_email()






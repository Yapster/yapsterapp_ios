from rest_framework.response import Response
from rest_framework.decorators import api_view
from notification.serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from notification.models import *
from django.utils import timezone
from yapster_utils import check_session

class LoadAllNotifications(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		print request
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				notification = user.functions.load_notifications(request['amount'],request['after'])
				print notification
				serialized = NotificationSerializer(notification,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
			else:
				notification = user.functions.load_notifications(request['amount'])
				print notification
				serialized = NotificationSerializer(notification,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
		else:
			return Response(check[0])

class LoadUnreadNotifications(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		print request
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				notification = user.functions.load_unread_notifications(request['amount'],request['after'])
				print notification
				serialized = NotificationSerializer(notification,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
			else:
				notification = user.functions.load_unread_notifications(request['amount'])
				print notification
				serialized = NotificationSerializer(notification,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
		else:
			return Response(check[0])

class NotificationsRead(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		print request
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			notifications_read = request['notifications_read']
			print notifications_read
			for notification_read in notifications_read:
				notification_read = Notification.objects.get(pk=notification_read)
				print notification_read.pk
				notification_read1 = notification_read.viewed()
			return Response({"valid":True,"message":"Notifications have been viewed."})
		else:
			return Response(check[0])

class NotificationsClicked(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		print request
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			notifications_clicked = request['notifications_clicked']
			for notification_clicked in notifications_clicked:
				notification_clicked = Notification.objects.get(pk=notification_clicked)
				notification_clicked1 = notification_clicked.clicked()
			return Response({"valid":True,"message":"Notifications have been clicked."})
		else:
			return Response(check[0])





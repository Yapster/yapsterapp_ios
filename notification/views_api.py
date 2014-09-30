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
				notifications = user.functions.load_notifications(request['amount'],request['after'])
				serialized = NotificationSerializer(notifications,data=self.request.DATA,many=True,context={'user':user})
				serialized_data = serialized.data
				for notification in notifications:
					notification.read()
				return Response(serialized_data)
			else:
				notifications = user.functions.load_notifications(request['amount'])
				serialized = NotificationSerializer(notifications,data=self.request.DATA,many=True,context={'user':user})
				serialized_data = serialized.data
				for notification in notifications:
					notification.read()
				return Response(serialized_data)
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
				serialized = NotificationSerializer(notification,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
			else:
				notification = user.functions.load_unread_notifications(request['amount'])
				serialized = NotificationSerializer(notification,data=self.request.DATA,many=True,context={'user':user})
				return Response(serialized.data)
		else:
			return Response(check[0])

class NotificationsRead(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			notifications_read = request['notifications_read']
			for notification_read in notifications_read:
				notification_read = Notification.objects.get(pk=notification_read)
				notification_read1 = notification_read.read()
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





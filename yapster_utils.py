from yap.models import *
from users.models import *

def check_session(user,session):
	check = user.session.check(session)
	if check['Valid'] and check['Message'] == "The session_id is up to date.":
		return (check,True)
	else:
		return (check,False)


def check_session_and_udid(user,session_id,session_udid):
	check = user.session.check_session_id_and_udid(session_id=session_id,session_udid=session_udid)
	if check['Valid'] and check['Message'] == "The session_id and udid is up to date.":
		return (check,True)
	else:
		return (check,False)


import datetime
def get_trending(minutes=60,amount=8):
	time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
	print time
	return Hashtag.objects.filter(date_created__gte=time).annotate(count=Count('tag_name')).order_by('count').distinct("tag_name")[:amount]


#When you're filtering and try to aggregate numbers and that we created fake likes, listens, reyaps.
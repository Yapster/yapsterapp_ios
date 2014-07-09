from django.contrib.auth.models import User
from users.models import *
from yap.models import *
from notifications.models import *
from stream.models import *
from location.models import *
from operator import itemgetter
import random
import datetime
import time
import csv

"""
IMPORTANT NOTE

when looking at likes, listens, and reyaps, always look at original_object
because reyap will not be null in order to keep the information of where 
it came from, but even though it will not be null, the action does not count
as a reyap action because it is placed on a like...ORIGINAL_OBJECT = FALSE IS 
ALWAYS ABOUT A YAP BUT FROM A REYAP
"""

user_created_date = datetime.datetime.now()
user_requested_date = user_created_date + datetime.timedelta(days=1)
miminum_yap_date = user_created_date + datetime.timedelta(seconds=300)
minimum_yap_action_date = user_requested_date + datetime.timedelta(seconds=300)
minimum_reyap_action_date = minimum_yap_action_date + datetime.timedelta(seconds=60)

print("starting first names")
with open('CSV_Database_of_First_Names.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	first_names = [x[0] for x in reader]

print("starting last names")
with open('CSV_Database_of_Last_Names.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	last_names = [x[0] for x in reader]

print("starting cities")
with open('cities.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	cities = [x[1] for x in reader]

print("starting on countries")
with open('countries.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	countries = [x[1] for x in reader]

print("starting on states")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states_names = [x[1] for x in reader]

print("starting on states_abbreviations")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states_abbreviations = [x[2] for x in reader]

print("starting on states_abbreviations")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states = [x[1] for x in reader]

print("starting on states_abbreviations")
with open('zip_code_database.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	zipcodes = [x[0] for x in reader]

print("starting words")
with open("/usr/share/dict/words","r") as f:
	words = [x.strip() for x in f.readlines()]

print len(words)

print(words[:10])

print "Starting hashtags"
with open('hashtags.csv','r') as f:
	reader = csv.reader(f)
	header = reader.next()
	hashtags = [x[1] for x in reader]


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

print("starting channels")
'''
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
#'''

import gc
profile_pictures = [
	'yapsterapp.com/paths/images/profile/1',
	'yapsterapp.com/paths/images/profile/2',
	'yapsterapp.com/paths/images/profile/3',
	'yapsterapp.com/paths/images/profile/4'
]

profile_pictures_cropped = [
	'yapsterapp.com/paths/images/cropped/profile/1',
	'yapsterapp.com/paths/images/cropped/profile/2',
	'yapsterapp.com/paths/images/cropped/profile/3',
	'yapsterapp.com/paths/images/cropped/profile/4',	
]

yap_images = [
	'yapsterapp.com/paths/images/yap/1',
	'yapsterapp.com/paths/images/yap/2',
	'yapsterapp.com/paths/images/yap/3',
	'yapsterapp.com/paths/images/yap/4'
]


def date_time_between(start,end):
	between = end - start
	seconds = (between.days * 24 * 60 * 60) + between.seconds
	random_seconds = random.randrange(seconds)
	return start + datetime.timedelta(seconds=random_seconds)

def date_between(start,end):
	between = end - start
	random_days = random.randint(0,between.days)
	return start + datetime.timedelta(days=random_days)

def rand(options,times=20):
	probabilities = options.values()
	while times > 0:
		random_number = random.random()
		threshold = 0
		answer = None
		for item in options.iteritems():
			threshold += item[1]
			if random_number <= threshold:
				answer = item[0]
				break
		print(answer)
		times -= 1

def incremented(item):
	#returns a dictionary with values that are probabilities'''
	range_ids = range(1,len(item)+1)
	size = len(range_ids)
	#x/1 + x/2 + ... + x/size = 1
	#x * sum([1/i for i in range_ids]) = 1
	x = 1.0/sum([1/float(i) for i in range_ids])
	#check to make sure it's right
	probabilities = [x/float(i) for i in range_ids]
	return dict(zip(range_ids,probabilities))

'''
def create_countries():
	print(countries)
	for country in countries:
		print country
		country_name = {
			'country':country
		}
		Countries.objects.create(**country_name)

create_countries()

def create_states():
	print(states)
	for state in states:
		print state
		state_name = {
			'us_state':state
		}
		USStates.objects.create(**state_name)

create_states()

def create_cities():
	print(cities)
	for city in cities:
		print city
		country = Countries.objects.get(pk=184)
		city_name = {
			'city'	:city,
			'country' :country,
		}
		print city_name
		Cities.objects.create(**city_name)

create_cities()




def create_zipcodes():
	print(zipcodes)
	for zipcode in zipcodes:
		print zipcode
		zipcode_number = {
			'us_zip_code':zipcode
		}
		USZIPCodes.objects.create(**zipcode_number)

create_zipcodes()

#'''
'''
def create_users():
	limit=30
	initial = limit
	user_hold = []
	while limit > 0:
		limit -= 1
		print limit
		seed1 = random.randint(0,len(first_names)-1)
		seed2 = random.randint(0,len(last_names)-1)
		#seed3 = random.randint(0,len(states)-1)
		#seed4 = random.randint(0,len(cities)-1)
		first_name = first_names[seed1]
		last_name = last_names[seed2]
		full_name = (first_name,last_name)
		same_name_number = user_hold.count(full_name)
		user_hold.append(full_name)
		if same_name_number < 1:
			username = first_name.lower() + '_' + last_name.lower()
		else:
			username = first_name.lower() + '_' + last_name.lower() + '_' + str(same_name_number)
		email = username + "@yapster.co"
		print limit
		password = username.lower()
		phone = ''
		gender_list = ['M','F','O']
		gender = random.choice(gender_list)
		if random.random() < 0.15:
			for x in range(10):
				phone += str(random.randint(0,9))
		if random.random() < 0.9:
			country = Countries.objects.get(pk=184)
			states_list = list(USStates.objects.all())
			state = random.choice(states_list)
			cities_list = list(Cities.objects.all())
			city = random.choice(cities_list)
		else:
			city = None
			state = None
			country = None
		print limit
		#random bday calculator
		earliest_bday = datetime.date(2000,1,1)
		oldest_bday = datetime.date(1950,1,1)
		date_of_birth = date_between(oldest_bday,earliest_bday)
		#create description
		description = ''
		print limit
		num_words = random.randint(10,20)
		print limit
		while num_words > 0:
			description += words[random.randint(0,len(words)-1)]
			if num_words > 1:
				description += " "
			num_words -= 1
		print limit
		image = profile_pictures[random.randint(0,len(profile_pictures)-1)]
		print limit
		image_cropped = profile_pictures_cropped[random.randint(0,len(profile_pictures_cropped)-1)]
		print limit
		pk = initial - limit
		print limit
		user = {
			'first_name'	:first_name,
			'last_name'		:last_name,
			'username'		:username,
			'email'			:email,
			'password'		:password,
			'gender'		:gender,
			'phone'			:phone,
			'user_city'		:city,
			'user_state'	:state,
			'user_country'	:country,
			'date_of_birth'	:date_of_birth
			}
		UserFunctions.create(**user)
		print(limit)
		print user

start = datetime.datetime.now()
create_users()
end = datetime.datetime.now()

print("users created in " + str(end-start))

#'''

users = list(User.objects.all())

'''
def make_followers():
	user_ids = [user.pk for user in users]
	if FollowerRequest.objects.all().exists():
		requesters = [l.user for l in FollowerRequest.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		user_copy = users
	for i,user in enumerate(user_copy):
		user_ids_copy = list(user_ids)
		user_ids_copy.remove(user.pk)
		#print len(user_keys)
		number_seed = random.randint(10,20)
		original_seed = number_seed
		print number_seed
		while number_seed > 0:
			seed = random.randint(0,len(user_ids_copy)-1)
			requested_user = user_ids_copy.pop(seed)
			user.functions.follow_request(requested_user)
			print(i, user.pk, number_seed, original_seed)
			number_seed -= 1
		print(str(user.pk) + " has finished")
		gc.collect()

start = datetime.datetime.now()
make_followers()
end = datetime.datetime.now()
print("followers created in " + str(end-start))
#'''

listeners = FollowerRequest.objects.all()
'''
print("starting yaps")

def make_yaps():
	if Yap.objects.all().exists():
		#requesters = [yap.user for yap in Yap.objects.all()]
		#user_copy = [user for user in users if user not in requesters]
		user_copy = users
	else:
		user_copy = users
	print ("starting yaps")
	for user in user_copy:
		print ("user chosen in user_copy",user)
		num_yaps = random.randint(5,10)
		print ("num_yaps",num_yaps)
		while num_yaps > 0:
			print ("num_yaps",num_yaps)
			#hashtag creation
			print ("user",user, num_yaps)
			if random.random() < 1.0:
				num_hashtags = random.randint(1,6)
				hashtags_flag = True
				list_of_hashtags = list(hashtags)
				yap_hashtags = random.sample(list_of_hashtags,num_hashtags)
			else:
				yap_hashtags = None
				hashtags_flag = False
			print(1)
			print ("user 1",user)
			#usertag creation
			if random.random() < 1.0:
				num_user_tags = random.randint(1,3)
				user_tags_flag = True
				users_clone = list(User.objects.filter(is_active=True).values('username'))
				print ("users_clone",users, num_user_tags)
				user_tags_chosen = random.sample(users_clone,num_user_tags)
				user_tags = []
				for user_tag in user_tags_chosen:
					user_tags.append(user_tag['username'])
			else:
				user_tags = None
				user_tags_flag = False
			print(2)
			print ("user 2",user)
			#title creation
			num_words = random.randint(1,3)
			title = ""
			while num_words > 0:
				seed = random.randint(0,len(words)-1)
				word = words[seed]
				if len(title + word) > 24:
					title = title.strip()
					break
				else:
					title += word
				if num_words > 1:
					title +=  " "
				num_words -= 1
			print(3)
			print ("user 3",user)
			if random.random() < 0.7:
				picture_flag = True
				number_of_yaps_currently = len(list(Yap.objects.filter(user=user,is_active=True)))
				picture_path = 'yapsterapp.com/paths/images/dsfsaf/' + str(user.pk) + "/" + str(number_of_yaps_currently + 1) + '/1'
			else:
				picture_path = None
				picture_flag = False
			print(4)
			print ("user 4",user)
			print ("user for audio_path",user)
			number_of_yaps_currently = len(list(Yap.objects.filter(user=user,is_active=True)))
			audio_path = 'yapsterapp.com/paths/audio/users/ddsafa/' + str(user.pk) + "/" + str(number_of_yaps_currently + 1)
			if random.random() < 1.0:
				channel_flag = True
				channel_list = list(Channel.objects.all())
				channel = random.choice(channel_list)
			else:
				channel = None
				channel_flag = False
			print(5)
			length = random.randint(7,40)
			#date_created = date_time_between(miminum_yap_date,datetime.datetime(2014,3,1,0,0,0))
			print ("user by yap",user)
			yap = {
				'hashtags_flag'		:hashtags_flag,
				#'hashtags'			:yap_hashtags,
				'user_tags_flag'	:user_tags_flag,
				#'user_tags'		:user_tags,
				'user'				:user,
				'audio_path'		:audio_path,
				'length'			:length,
				'picture_flag'		:picture_flag,
				'picture_path'		:picture_path,
				'channel_flag'		:channel_flag,
				'channel'			:channel,
				'title'				:title,
			}
			print(yap)
			obj = Yap.objects.create(**yap)
			if hashtags_flag:
				obj.add_hashtags(hashtags=yap_hashtags)
				print("done")
			if user_tags_flag:
				obj.add_user_tags(user_tags)
			num_yaps -= 1

		print str(user.pk) + " has finished"

	gc.collect()

make_yaps()

#'''

yaps = list(Yap.objects.all())
users = list(User.objects.all())
'''
def make_reyaps():
	for_checking = []
	if Reyap.objects.all().exists():
		requesters = [reyap.user for reyap in Reyap.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		user_copy = users
	print ("starting reyaps")
	for user in user_copy:
		num_reyaps = random.randint(25,50)
		print ("num_reyaps", num_reyaps)
		#userlikes = [like.yap.pk for like in user.likes.all()]
		possible_yaps = [post.yap.pk for post in Stream.objects.filter(user=user) if not post.reyap_flag]
		possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
		while num_reyaps > 0:
			print("user", user)
			print ("num_reyaps", num_reyaps)
			print ("possible_reyaps", possible_reyaps)
			print ("possible_yaps", possible_yaps)
			if random.random() < 0.5 and len(possible_reyaps) > 0:
				target = 'reyap'
			else:
				if len(possible_yaps) > 0:
					target = 'yap'
				else:
					target = "reyap"
			print target
			if target == 'yap':
				seed = random.choice(possible_yaps)
				#print ("possible_yaps", possible_yaps)
				print ("seed", seed)
				yap = Yap.objects.get(pk=seed)
				if (yap.pk,user.pk) in for_checking:
					continue
				else:   
					for_checking.append((yap.pk,user.pk))
					reyap = None
					reyap_flag = False
					new_reyap = {
						'yap'				:yap,
						'user'				:user,
						'reyap_flag'		:reyap_flag,
						'reyap_reyap'		:reyap
					}
					print ("new_reyap", new_reyap)
					Reyap.objects.create(**new_reyap)
					num_reyaps -= 1
			elif target == 'reyap' and possible_reyaps != []:				
				reyap_chosen = random.choice(possible_reyaps)
				reyap = Reyap.objects.get(pk=reyap_chosen)
				yap = reyap.yap
				if (yap.pk,user.pk) in for_checking:
					continue
				reyap_flag=True
				if not (yap.pk,user.pk) in for_checking:
					for_checking.append((yap.pk,user.pk))
					fake_needed = True
					try:
						possible_yaps.remove(reyap.yap.pk)
					except:
						pass
				else:
					fake_needed = False
				print ("reyap", reyap)
				#print ("user.pk, yap.pk", user.pk, yap.pk)
				#print ("new_reyap", new_reyap)
				reyap.reyap(user)
				num_reyaps -= 1
			#print num_reyaps
			elif possible_reyaps == []:
				print("the possible_reyaps queryset is empty.") 
		print ("num_reyaps", num_reyaps)
			#print num_reyaps
	print(str(user.pk) + " has finished")
	gc.collect()


start = datetime.datetime.now()
end = datetime.datetime.now()
make_reyaps()
print("Reyaps created in " + str(end-start))
#'''
reyaps = list(Reyap.objects.all())
users = list(User.objects.all())

'''
def make_likes():
	for_checking = []
	if Like.objects.all().exists():
		requesters = [like.user for like in Like.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		reyaps = list(Reyap.objects.all())
		user_copy = users
	for user in user_copy:
		num_likes = random.randint(50,75)
		#userlikes = [like.yap.pk for like in user.likes.all()]
		possible_yaps = [post.yap.pk for post in Stream.objects.filter(user=user) if not post.reyap_flag]
		possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
		while num_likes > 0:
			if random.random() < 0.5:
				target = 'reyap'
			else:
				target = 'yap'
			print target
			if target == 'yap':
				seed = random.choice(possible_yaps)
				print possible_yaps
				print ("seed", seed)
				yap = Yap.objects.get(pk=seed)
				if (yap.pk,user.pk) in for_checking:
					continue
				else:	
					for_checking.append((yap.pk,user.pk))
					reyap = None
					reyap_flag = False
					like = {
					'yap'			:yap,
					'reyap_flag'	:reyap_flag,
					'reyap'			:reyap,
					'user'			:user
					}
					print user.pk, yap.pk
					print like
					Like.objects.create(**like)
			elif target == 'reyap' and possible_reyaps != []:
				#possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
				
				print possible_reyaps
				reyap_chosen = random.choice(possible_reyaps)
				reyap = Reyap.objects.get(pk=reyap_chosen)
				yap = reyap.yap
				if (yap.pk,user.pk) in for_checking:
					continue
				reyap_flag=True
				if not (yap.pk,user.pk) in for_checking:
					for_checking.append((yap.pk,user.pk))
					fake_needed = True
					try:
						possible_yaps.remove(reyap.yap.pk)
					except:
						pass
				else:
					fake_needed = False
				like = {
				'yap'			:yap,
				'reyap_flag'	:reyap_flag,
				'reyap'			:reyap,
				'user'			:user,
				}
				print user.pk, yap.pk
				print like
				reyap.like(user)
			num_likes -= 1 
			print ("num_likes")
			print num_likes
		print(str(user.pk) + " has finished")
		gc.collect()

make_likes()

#	sorted_listens = sorted(listens)
#	final = []
#	for pk,listen in enumerate(sorted_listens):
#		actual_listen = listen[1]
#		actual_listen['id'] = pk
#		final.append(actual_listen)
#	return final

start = datetime.datetime.now()
end = datetime.datetime.now()
print("Likes created in " + str(end-start))

#'''

likes = Like.objects.all()
users = list(User.objects.all())

'''
def make_listens():
	for_checking = []
	if Listen.objects.all().exists():
		requesters = [listen.user for listen in Listen.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		user_copy = users
	for user in user_copy:
		num_listens = random.randint(100,150)
		#userlikes = [like.yap.pk for like in user.likes.all()]
		possible_yaps = [post.yap.pk for post in Stream.objects.filter(user=user) if not post.reyap_flag]
		possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
		while num_listens > 0:
			if random.random() < 0.5:
				target = 'reyap'
			else:
				target = 'yap'
			print target
			if target == 'yap':
				seed = random.choice(possible_yaps)
				print possible_yaps
				print ("seed", seed)
				yap = Yap.objects.get(pk=seed)
				if (yap.pk,user.pk) in for_checking:
					continue
				else:	
					for_checking.append((yap.pk,user.pk))
					reyap = None
					reyap_flag = False
					listen = {
					'yap'			:yap,
					'reyap_flag'	:reyap_flag,
					'reyap'			:reyap,
					'user'			:user
					}
					print user.pk, yap.pk
					print listen
					Listen.objects.create(**listen)
			elif target == 'reyap' and possible_reyaps != []:
				#possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
				print possible_reyaps
				reyap_chosen = random.choice(possible_reyaps)
				reyap = Reyap.objects.get(pk=reyap_chosen)
				yap = reyap.yap
				if (yap.pk,user.pk) in for_checking:
					continue
				reyap_flag=True
				if not (yap.pk,user.pk) in for_checking:
					for_checking.append((yap.pk,user.pk))
					fake_needed = True
					try:
						possible_yaps.remove(reyap.yap.pk)
					except:
						pass
				else:
					fake_needed = False
				listen = {
				'yap'			:yap,
				'reyap_flag'	:reyap_flag,
				'reyap'			:reyap,
				'user'			:user,
				}
				print user.pk, yap.pk
				print listen
				reyap.listen(user)
			num_listens -= 1 
			print ("num_listens")
			print num_listens
		print(str(user.pk) + " has finished")
		gc.collect()

make_listens()

start = datetime.datetime.now()
listens = make_listens()
end = datetime.datetime.now()
print("Listens created in " + str(end-start))

#'''


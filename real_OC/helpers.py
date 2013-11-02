import urllib2, urllib
from bs4 import BeautifulSoup
from open_rooms.views import *

all_days = {'M': 'Monday',
			'Tu': 'Tuesday',
			'W': 'Wednesday',
			'Th': 'Thursday',
			'F': 'Friday'}

def set_building(errors, form):
	if 'building' in errors:
		bldg = False
	else:
		bldg = form.cleaned_data['building']
	return bldg

def set_num(errors, form):
	if 'number' in errors:
		num = False
	else:
		num = form.cleaned_data['number']
	return num

def set_time(errors, form):
	if 'time' in errors:
		time = False
	else:
		time = form.cleaned_data['time']
	return time

def set_day(errors, form):
	if 'day' in errors:
		day = False
	else:
		day = form.cleaned_data['day']
	return day

def determine_request(bldg, time, day, num):
	#Quadruple Input
	if bldg and time and day and num:
		return get_building_time_day_number(bldg, time, day, num)
	#Triple Input
	elif bldg and time and day:
		return get_building_time_day(bldg, time, day)
	elif bldg and time and num:
		return get_building_time_number(bldg, time, num)
	elif bldg and day and num:
		return get_building_day_number(bldg, day, num)
	elif time and day and num:
		return get_day_time_number(day, time, num)
	#Double Input
	elif time and day:
		return get_time_day(time, day)
	elif bldg and day:
		return get_building_day(bldg, day)
	elif bldg and time:
		return get_building_time(bldg, time)
	elif bldg and num:
		return get_building_number(bldg, num)
	elif time and num:
		return get_time_number(time, num)
	elif day and num:
		return get_day_number(day, num)
	#Single Input
	elif bldg:
		return get_building(bldg)
	elif time:
		return get_time(time)
	elif day:
		return get_day(day)
	elif num:
		return get_number(num)
	#else
		#throw error


"""
	Returns the source code of a web page
"""
def get_page(url, post_data=''):
    try:
        return urllib2.urlopen(url, urllib.urlencode(post_data)).read()
    except:
        return ''


def add_to_db(semester, bldg):
	building = get_building_source(semester, bldg)
	soup = BeautifulSoup(building)
	tags = get_necessary_tags(soup)
	room_to_associations = separate_into_rows(tags)
	for row in room_to_associations:
		day_and_hour_text = strip_building(room_to_associations[row][3].contents[0])
		room_text = strip_building(room_to_associations[row][4].contents[0])
		room_number, room_building = room_text.split(' ', 1)
		room = create_room(room_number, room_building)
		timeslots = create_timeslots(day_and_hour_text)
		associate_room_and_times(room, timeslots)

def create_room(room_number, room_building):
	if Room.objects.filter(building=room_building, number=room_number):
		pass
	else:
		Room(building=room_building, number=room_number).save()
	return Room.objects.filter(building=room_building, number=room_number)

def create_timeslots(day_and_hour_text):
	#parse day_and_hour_text
	times = parse_time(day_and_hour_text)
	timeslots = []
	#create timeslot
	for day in times.keys():
		for time in times[day]:
			if TimeSlot.objects.filter(day=day, time=time[:-1], ap=time[-1]):
				pass
			else:
				TimeSlot(day=day,time=time[:-1],ap=time[-1]).save()
			timeslots.append(TimeSlot.objects.filter(day=day, time=time[:-1], ap=time[-1]))
	return timeslots
	
def associate_room_and_times(room, timeslots):
	for time in timeslots:
		for t in time:
			t.room.add(room[0])

def parse_time(day_and_hour_text):
	#output dictionary mapping key 'day' to a list of half hours and if AM or PM
	# >>> parse_time('M 1-2P')
	# {'M' : [1P, 1:30P]}
	# >>> parse_time('MTuWTh 11-1P')
	# {'M': ['11A', '11:30A', '12P', '12:30P'], 'W': ['11A', '11:30A', '12P', '12:30P'],  
	#  'Tu': ['11A', '11:30A', '12P', '12:30P'], 'Th': ['11A', '11:30A', '12P', '12:30P']}
	days_and_times = {}
	days, times = day_and_hour_text.split(' ', 1)
	times_list = split_times(times)
	for d in split_days(days):
		days_and_times[d] = []
		for time in times_list:
			days_and_times[d].append(time)
	return days_and_times

def split_days(days):
	#returns a list of all days
	# >>> split_days('MTuWTh')
	# ['M', 'Tu', 'W', 'Th']
	# >>> split_days('TuThF')
	# ['Tu', 'Th', 'F']
	results = []
	i = 0
	while i < len(days):
		if days[i] in all_days:
			results.append(all_days[days[i]])
		elif days[i: i+2] in all_days:
			results.append(all_days[days[i: i+2]])
		i += 1
	return results

def split_times(times):
	#returns a list of all times 930-11P
	# >>> split_times('1130-1P')
	# ['1130P', '12P', '1230P']
	# >>> split_times('4-5P')
	# ['4P', '430P']
	results = []
	begin_time, end_time_ap = times.split('-')
	end_time = end_time_ap[:-1]
	ap = end_time_ap[-1]
	while (begin_time != end_time):
		if len(begin_time) == 3:
			#between 130 and 930 and starts on the half hour
			current_ap = is_a_or_p(begin_time,end_time,ap)
			results.append(begin_time + current_ap)
			begin_time = str(int(begin_time[0]) + 1)
		elif len(begin_time) == 4:
			#1030 or 1130 or 1230
			current_ap = is_a_or_p(begin_time,end_time,ap)
			results.append(begin_time + current_ap)
			if begin_time == '1130':
				begin_time = '12'
			elif begin_time == '1230':
				begin_time = '1'
			else:
				begin_time = '11'
		else:
			current_ap = is_a_or_p(begin_time,end_time,ap)
			results.append(begin_time + current_ap)
			begin_time = begin_time + '30'
	return results

def is_a_or_p(begin_time, end_time, ap):
	if len(begin_time) == 4 or len(begin_time) == 2:
		begin_time_hour = begin_time[:2]
	else:
		begin_time_hour = begin_time[0]
	if len(end_time) == 4 or len(end_time) == 2:
		end_time_hour = end_time[:2]
	else:
		end_time_hour = end_time[0]
	if end_time == '12':
		ap = 'A'
		return ap
	if end_time == '1230':
		if begin_time == '12':
			ap = 'P'
		else:
			ap = 'A'
		return ap
	if begin_time_hour == end_time_hour:
		return ap
	if int(begin_time_hour) < int(end_time_hour) or begin_time_hour == '12':
		pass
	else:
		if ap == 'P':
			ap = 'A'
		#will never be the case that a class goes from PM to AM
	return ap

def get_necessary_tags(soup):
	tags = []
	for tag in soup.find_all('font'):
		if tag['size'] == '-4':
			tags.append(tag)
	for tag in tags:
		if tag.b:
			tags.remove(tag)
		else:
			pass
	return tags

def separate_into_rows(tags_list):
	room_to_associations = {}
	j = 0
	z = 0
	for tag in tags_list:
		if j in room_to_associations:
			room_to_associations[j].append(tag)
		else:
			room_to_associations[j] = [tag]
		z += 1
		if z == 10:
			j += 1
			z = 0
	return room_to_associations

def strip_building(content):
	return content.strip().encode('ascii')

"""
	Returns all matches of a BUILDING in a given SEMESTER
	equivalent content to viewing the url at:
	http://osoc.berkeley.edu/OSOC/osoc?p_term={{SEMESTER}}&p_bldg={{BUILDING}}&p_print_flag=Y
"""
def get_building_source(semester, building):
	#semester should be two chars: SP, SU, or FL
	#one path for all requests
	path = 'http://osoc.berkeley.edu/OSOC/osoc'
	post_data = [('p_term', semester), ('p_print_flag', 'Y'), ('p_bldg', building)]
	source = get_page(path, post_data)
	return source


"""
	Replaces spaces with '+'. Needed for query parameter passing.
"""
def format(abbr):
	#Need to send query paramaters with + instead of ' '
	#
	#For all items in a list
	#	If there are spaces separating words
	#		replace the space with a +
	abbr = abbr.replace(' ', '+')


def store_all_rooms(semester):
	full_name, abbreviations = building_lists()
	for abbr in abbreviations:
		format(abbr)
		add_to_db(semester, abbr)

"""
	Returns 2 lists of building names: full names and abbreviations

	full_name, abbr = building_lists()
"""
def building_lists():
    source = get_page("http://registrar.berkeley.edu/Default.aspx?PageID=bldgabb.html")
    #make 2 lists
    full_name = []
    abbr = []

    #look for tags starting with <td valign
    target = "<td valign"
    target_index = source.find(target)
    content = source[target_index:]

    #extract building names
    while target_index != -1:
        word_start = content.find(">") + 1
        word = content[word_start:content.find("</td>")]
        if word.isupper() or word == "FOOTHILL 1" or word == "FOOTHILL 4":
            abbr.append(word)
        else:
            full_name.append(word)
        content = content[content.find("/td"):]
        target_index = content.find(target)
        content = content[target_index:]
    full_name.append("Li Ka Shing Center")
    abbr.append("LI KA SHING")
    return full_name, abbr

from open_rooms.models import *
from open_rooms.helpers import *
from datetime import *

#Default to input of TODAY if no day input is provided by user
#SINGLE INPUT
#Output dictionaries mapping {Room, [Timeslot1, Timeslot2...]}

def get_building(bldg, ap):
	results = {}
	today = convert_to_day(datetime.today().weekday())
	for room in Room.objects.filter(building=bldg.upper()):
		results[room] = []
		for time in room.timeslot_set.all():
			if str(time.day) == today and str(time.ap) == ap:
					results[room].append(time)
	return results

def get_time(time, ap):
	results = {}
	today = convert_to_day(datetime.today().weekday())
	time_slot = TimeSlot.objects.filter(day=today).exclude(time=time)
	for room in Room.objects.filter(timeslot__in=time_slot):
		results[room] = []
		for time in room.timeslot_set.all():
			if str(time.day) == today and str(time.ap) == ap:
				results[room].append(time)
	print results
	return results

def get_number(num, ap):
	results = {}
	today = convert_to_day(datetime.today().weekday())
	for room in Room.objects.filter(timeslot__day__exact=today,number=num):
		results[room] = []
		for time in room.timeslot_set.all():
			if str(time.day) == today and str(time.ap) == ap:
				results[room].append(time)
	return results

def get_day(day, ap):
	results = {}
	for room in Room.objects.filter(timeslot__day__exact=day):
		results[room] = []
		for time in room.timeslot_set.all():
			if str(time.day) == day and str(time.ap) == ap:
				results[room].append(time)
	return results

#DOUBLE INPUT
from open_rooms.models import *
from open_rooms.helpers import *
from datetime import *
from django.http import HttpResponse

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
	will_this_room_work = True
	results = {}
	today = convert_to_day(datetime.today().weekday())
	#time_slot = TimeSlot.objects.filter(day=today).exclude(time=time)
	for room in Room.objects.filter(timeslot__day__exact=today).distinct():
		results[room] = []
		for timeslot in room.timeslot_set.filter(day=today):
			if str(timeslot.time) == str(time) and str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
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
	for room in Room.objects.filter(timeslot__day__exact=day).distinct():
		results[room] = []
		for time in room.timeslot_set.all():
			if str(time.day) == day and str(time.ap) == ap:
				results[room].append(time)
	return results

#DOUBLE INPUT

def get_time_day(time, day, ap):
	time_slots = TimeSlot.objects.filter(day=day).exclude(time=time)
	return Room.objects.filter(timeslot__in=time_slots).distinct()
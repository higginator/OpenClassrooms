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
	will_this_room_work = True
	results = {}
	today = convert_to_day(datetime.today().weekday())
	#time_slot = TimeSlot.objects.filter(day=today).exclude(time=time)
	time_slot = TimeSlot.objects.filter(day=today)
	for room in Room.objects.filter(timeslot__in=time_slot).distinct():
		#results[room] = []
		times_list = []
		for timeslot in room.timeslot_set.filter(day=today):
			#if str(time.day) == today and str(time.ap) == ap:
			#	results[room].append(time)
			if str(timeslot.time) == str(time) and str(timeslot.ap) == str(ap):
				will_this_room_work = False
				break
			else:
				times_list.append(timeslot)
		if will_this_room_work:
			results[room] = []
			results[room].extend(times_list)
		else:
			will_this_room_work = True
		del times_list
	#print results
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
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
	results = {}
	today = convert_to_day(datetime.today().weekday())
	for room in Room.objects.filter(timeslot__day__exact=today).distinct():
		results[room] = []
		for timeslot in room.timeslot_set.filter(day=today):
			if str(timeslot.time) == str(time) and str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
		if len(results[room]) == 1:
			del results[room]
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

def get_building_number(bldg, num, ap):
	results = {}
	today = convert_to_day(datetime.today().weekday())
	for room in Room.objects.filter(building=bldg.upper(), number=num):
		results[room] = []
		for time in room.timeslot_set.all():
			if str(time.day) == today and str(time.ap) == ap:
				results[room].append(time)
	return results

def get_building_day(bldg, day, ap):
	results = {}
	for room in Room.objects.filter(building=bldg.upper()):
		results[room] = []
		for time in room.timeslot_set.all():
			if str(time.day) == day.capitalize() and str(time.ap) == ap:
				results[room].append(time)
	return results

def get_building_time(bldg, time, ap):
	results = {}
	today = convert_to_day(datetime.today().weekday())
	for room in Room.objects.filter(building=bldg.upper()):
		results[room] = []
		for timeslot in room.timeslot_set.all():
			if str(timeslot.time) == str(time) and str(timeslot.ap) == str(ap) and str(timeslot.day) == today:
				results[room].append(timeslot)
		if len(results[room]) == 1:
			del results[room]
	return results

def get_time_number(time, num, ap):
	results = {}
	today = convert_to_day(datetime.today().weekday())
	for room in Room.objects.filter(number=num):
		results[room] = []
		for timeslot in room.timeslot_set.all():
			if str(timeslot.time) == str(time) and str(timeslot.ap) == str(ap) and str(timeslot.day) == today:
				results[room].append(timeslot)
		if len(results[room]) == 1:
			del results[room]
	return results

def get_day_number(day, num, ap):
	results = {}
	for room in Room.objects.filter(number=num):
		results[room] = []
		for timeslot in room.timeslot_set.all():
			if str(timeslot.day) == day.capitalize() and str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
	return results

def get_time_day(time, day, ap):
	results = {}
	for room in Room.objects.filter(timeslot__day__exact=day.capitalize()).distinct():
		results[room] = []
		for timeslot in room.timeslot_set.filter(day=day.capitalize()):
			if str(timeslot.time) == str(time) and str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
		if len(results[room]) == 1:
			del results[room]
	return results

#TRIPLE INPUT

def get_building_time_day(bldg, time, day, ap):
	results = {}
	for room in Room.objects.filter(building=bldg.upper()):
		results[room] = []
		for timeslot in room.timeslot_set.filter(day=day.capitalize()):
			if str(timeslot.time) and str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
		if len(results[room]) == 1:
			del results[room]
	return results

def get_building_time_number(bldg, time, num, ap):
	results = {}
	for room in Room.objects.filter(building=bldg.upper(), number=num):
		results[room] = []
		for timeslot in room.timeslot_set.filter(time=time):
			if str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
	return results

def get_building_day_number(bldg, day, num, ap):
	results = {}
	for room in Room.objects.filter(building=bldg.upper(), number=num):
		results[room] = []
		for timeslot in room.timeslot_set.filter(day=day.capitalize()):
			if str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
	return results

def get_day_time_number(day, time, num, ap):
	results = {}
	for room in Room.objects.filter(number=num):
		results[room] = []
		for timeslot in room.timeslot_set.filter(day=day.capitalize()):
			if str(timeslot.time) == str(time) and str(timeslot.ap) == str(ap):
				results[room].append(timeslot)
		if len(results[room]) == 1:
			del results[room]
	return results

#QUADRUPLE INPUT

def get_building_time_day_number(bldg, time, day, num, ap):
	results = {}
	for room in Room.objects.filter(building=bldg.upper(), number=num):
		results[room] = []
		for timeslot in room.timeslot_set.filter(day=day.capitalize()):
			if str(timeslot.ap) == str(ap) and str(timeslot.time) == str(time):
				results[room].append(timeslot)
	return results

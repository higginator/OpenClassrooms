# Create your views here.
from open_rooms.models import *
from open_rooms.helpers import *
from datetime import *

#Default to input of TODAY if no day input is provided by user
#SINGLE INPUT

def get_building(request, bldg):
	return Room.objects.filter(building=bldg)

def get_time(request, input_time):
	today = convert_to_day(datetime.today().weekday())
	return TimeSlot.objects.filter(time=input_time,day=today)

def get_day(request, input_day):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(day=input_day)
	for time in time_slots:
		desired_rooms.extend(time.room.all())
	return desired_rooms

def get_number(request, num):
	desired_rooms = []
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(day=today)
	for time in time_slots:
		for room in time.room.all():
			if room.number == num:
				desired_rooms.append(room)
	return desired_rooms

#DOUBLE INPUT

def get_time_day(request,input_time, input_day):
	return TimeSlot.objects.filter(time=input_time, day=input_day)

def get_building_day(request, bldg, input_day):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.building == bldg:
				desired_rooms.append(bldg)
	return desired_rooms

def get_building_time(request, bldg, input_time):
	desired_rooms = []
	today = convert_to_day(datetime.today().weekday())
	rooms = Room.objects.filter(building=bldg)
	for room in rooms:
		for time in room.timeslot_set.all():
			if time.time == input_time and time.day == today:
				desired_rooms.append(room)
	return desired_rooms

def get_building_number(request, bldg, num):
	return Room.objects.filter(building=bldg, number=num)

def get_time_number(request, input_time, num):
	desired_rooms = []
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(time=input_time, day=today)
	for time in time_slots:
		for room in time.room.all():
			if room.building == bldg and room.number == num:
				desired_rooms.append(room)
	return desired_rooms

def get_day_number(request, input_day, num):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.number == num:
				desired_rooms.append(room)
	return desired_rooms

#TRIPLE INPUT

def get_building_time_day(request, bldg, input_time, input_day):
	desired_rooms = []
	rooms = Room.objects.filter(building=bldg)
	for room in rooms:
		for time in room.timeslot_set.all():
			if time.time == input_time and time.day == input_day:
				desired_rooms.append(room)
	return desired_rooms

def get_building_time_number(request, bldg, input_time, num):

def get_building_day_number(request, bldg, input_day, num):

def get_day_time_number(request, input_day, input_time, num):

#QUADRUPLE INPUT

def get_building_time_day_number(request, bldg, input_time, input_day, num):

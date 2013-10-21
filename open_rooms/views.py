from open_rooms.models import *
from open_rooms.helpers import *
from datetime import *

#Default to input of TODAY if no day input is provided by user
#SINGLE INPUT

def get_building(bldg):
	return Room.objects.filter(building=bldg)

def get_time(input_time):
	today = convert_to_day(datetime.today().weekday())
	return TimeSlot.objects.filter(time=input_time,day=today)

def get_day(input_day):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(day=input_day)
	for time in time_slots:
		desired_rooms.extend(time.room.all())
	return desired_rooms

def get_number(num):
	desired_rooms = []
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(day=today)
	for time in time_slots:
		for room in time.room.all():
			if room.number == num:
				desired_rooms.append(room)
	return desired_rooms

#DOUBLE INPUT

def get_time_day(input_time, input_day):
	return TimeSlot.objects.filter(time=input_time, day=input_day)

def get_building_day(bldg, input_day):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.building == bldg:
				desired_rooms.append(bldg)
	return desired_rooms

def get_building_time(bldg, input_time):
	desired_rooms = []
	today = convert_to_day(datetime.today().weekday())
	rooms = Room.objects.filter(building=bldg)
	for room in rooms:
		for time in room.timeslot_set.all():
			if time.time == input_time and time.day == today:
				desired_rooms.append(room)
	return desired_rooms

def get_building_number(bldg, num):
	return Room.objects.filter(building=bldg, number=num)

def get_time_number(input_time, num):
	desired_rooms = []
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(time=input_time, day=today)
	for time in time_slots:
		for room in time.room.all():
			if room.number == num:
				desired_rooms.append(room)
	return desired_rooms

def get_day_number(input_day, num):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.number == num:
				desired_rooms.append(room)
	return desired_rooms

#TRIPLE INPUT

def get_building_time_day(bldg, input_time, input_day):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(time=input_time, day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.building == bldg:
				desired_rooms.append(room)
	return desired_rooms

def get_building_time_number(bldg, input_time, num):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(time=input_time)
	for time in time_slots:
		for room in time.room.all():
			if room.building == bldg and room.number == num:
				desired_rooms.append(room)
	return desired_rooms

def get_building_day_number(bldg, input_day, num):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.building == bldg and room.number == num:
				desired_rooms.append(room)
	return desired_rooms

def get_day_time_number(input_day, input_time, num):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(time=input_time, day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.number == num:
				desired_rooms.append(room)
	return desired_rooms

#QUADRUPLE INPUT

def get_building_time_day_number(bldg, input_time, input_day, num):
	desired_rooms = []
	time_slots = TimeSlot.objects.filter(time=input_time, day=input_day)
	for time in time_slots:
		for room in time.room.all():
			if room.building == bldg and room.number == num:
				desired_rooms.append(room)
	return desired_rooms
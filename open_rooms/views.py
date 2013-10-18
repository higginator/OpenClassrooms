# Create your views here.
from open_rooms.models import *
from open_rooms.helpers import *
from datetime import *

def get_building(request, bldg):
	return Room.objects.filter(building=bldg)

def get_time(request, input_time):
	return TimeSlot.objects.filter(time=input_time)

#def get_day(request, input_day):
#	timeslots = TimeSlot.objects.filter(day=input_day)
#	for time in timeslots:
	#
	#maybe dont allow this as only input

#def get_time_day(request,input_time, input_day):

#def get_building_day(request, bldg, input_day):

def get_building_time_today(request, bldg, input_time):
	desired_rooms = []
	today = convert_to_day(datetime.today().weekday())
	rooms = Room.objects.filter(building=bldg)
	for room in rooms:
		for time in room.timeslot_set.all():
			if str(time.time) == input_time and str(time.day) == today:
				desired_rooms.append(room)
	return desired_rooms

def get_building_time_day(request, bldg, input_time, input_day):
	desired_rooms = []
	rooms = Room.objects.filter(building=bldg)
	for room in rooms:
		for time in room.timeslot_set.all():
			if str(time.time) == input_time and str(time.day) == input_day:
				desired_rooms.append(room)
	return desired_rooms
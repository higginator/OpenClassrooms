# Create your views here.

def building_rooms(request, bldg):
	Room.objects.filter(building=bldg)

def building_and_time_rooms(request, bldg, input_time):
	desired_rooms = []
	rooms = Room.objects.filter(building=bldg)
	for room in rooms:
		for time in room.timeslot_set.all():
			if str(time.time) == input_time:
				desired_rooms.append(room)

def building_and_time_and_day(request, bldg, input_time, input_day):
	desired_rooms = []
	rooms = Room.objects.filter(building=bldg)
	for room in rooms:
		for time in room.timeslot_set.all():
			if str(time.time) == input_time and str(time.day) == input_day:
				desired_rooms.append(room)

def building_and_time_and_day_and_date(request, bldg, input_time, input_day, date):
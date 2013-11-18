from open_rooms.models import *
from open_rooms.helpers import *
from datetime import *

#Default to input of TODAY if no day input is provided by user
#SINGLE INPUT

def get_building(bldg, ap):
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(day=today).exclude(ap=ap)
	return Room.objects.filter(timeslot__in=time_slots, building=bldg.upper())

def get_time(input_time, ap):
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(day=today).exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots)

def get_day(input_day, ap):
	return Room.objects.filter(timeslot__day__exact=input_day)

def get_number(num, ap):
	today = convert_to_day(datetime.today().weekday())
	return Room.objects.filter(timeslot__day__exact=today,number=num)

#DOUBLE INPUT

def get_time_day(input_time, input_day):
	time_slots = TimeSlot.objects.filter(day=input_day).exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots)

def get_building_day(bldg, input_day):
	time_slots = TimeSlot.objects.filter(day=input_day)
	return Room.objects.filter(timeslot__in=time_slots,building=bldg)

def get_building_time(bldg, input_time):
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(day=today).exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots,building=bldg)

def get_building_number(bldg, num):
	return Room.objects.filter(building=bldg, number=num)

def get_time_number(input_time, num):
	today = convert_to_day(datetime.today().weekday())
	time_slots = TimeSlot.objects.filter(day=today).exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots,number=num)

def get_day_number(input_day, num):
	return Room.objects.filter(timeslot__day__exact=input_day,number=num)


#TRIPLE INPUT

def get_building_time_day(bldg, input_time, input_day):
	time_slots = TimeSlot.objects.filter(day=input_day).exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots,building=bldg)

def get_building_time_number(bldg, input_time, num):
	time_slots = TimeSlot.objects.exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots,building=bldg,number=num)


def get_building_day_number(bldg, input_day, num):
	time_slots = TimeSlot.objects.filter(day=input_day)
	return Room.objects.filter(timeslot__in=time_slots,building=bldg,number=num)


def get_day_time_number(input_day, input_time, num):
	time_slots = TimeSlot.objects.filter(day=input_day).exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots,number=num)
	

#QUADRUPLE INPUT

def get_building_time_day_number(bldg, input_time, input_day, num):
	time_slots = TimeSlot.objects.filter(day=input_day).exclude(time=input_time)
	return Room.objects.filter(timeslot__in=time_slots,building=bldg,number=num)
	

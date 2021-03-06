from django.db import models

# Create your models here.
class Room(models.Model):
	building = models.CharField(max_length=50)
	number = models.CharField(max_length=10)

	def __unicode__(self):
		return '%s%s' % (self.number, self.building)

class TimeSlot(models.Model):
	time = models.CharField(max_length=10)
	day = models.CharField(max_length=15)
	ap = models.CharField(max_length=1)
	room = models.ManyToManyField(Room)

	def __unicode__(self):
		return self.day + ' ' + self.time

	class Meta:
		ordering = ('time',)

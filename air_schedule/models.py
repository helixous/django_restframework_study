from django.db import models


# Create your models here.
class AirSchedule(models.Model):
    arrival_time = models.DateTimeField(max_length=500)
    departure_time = models.DateTimeField(max_length=500)
    navigation_section = models.CharField(max_length=100)
    operating_time = models.CharField(max_length=100)
    airplane_type = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "air_schedules"
        ordering = ('created',)

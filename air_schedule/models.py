from django.db import models


# Create your models here.
class AirSchedule(models.Model):
    # userId필드는 특정유저에게 해당되는 운항스케쥴이라는 개념을 나타내는 필드입니다.
    # 외래키로 작성하는것이 보통이지만 그냥 User테이블의 userId 필드를 참조함을 나타내도록 하겠습니다.
    userId = models.UUIDField()
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

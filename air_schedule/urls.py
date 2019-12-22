from django.urls import path, include
from .views import *

urlpatterns = [
    path("register-airschedule", registerAirSchedule),
    path("get-airschedule-list", getAirScheduleList),
]

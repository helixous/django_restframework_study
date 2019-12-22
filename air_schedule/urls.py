from django.urls import path, include
from .views import *

# views.py에 있는 api함수들을 매칭시켜줍니다.
urlpatterns = [
    path("register-airschedule", registerAirSchedule),
    path("get-airschedule-list", getAirScheduleList),
]

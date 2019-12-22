from django.urls import path, include
from .views import *

urlpatterns = [
    path("register-user", registerUser),
    path("get-user-info", getUserInfo),
    # path("find/nick/<nickname>", findByNickname),
    # path("find/name/<name>", findByName),
]

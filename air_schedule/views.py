from django.shortcuts import render
import json
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from .models import AirSchedule
from .serializers import *


# Create your views here.


# api_view데코레이터는 함수형뷰 위에 작성해주시면되며,
# 메소드를 제한해주는 역할 및 레스트프레임워크 템플릿 형태의 화면을 렌더링할수 있도록 지원해줍니다.
# 다음 형태는 POST 메소드만 허용한다는 것을 의미합니다.
@api_view(["POST"])
def registerAirSchedule(request):
    # 들어온 api 요청이 형식을 만족하는지 검증해야합니다.
    # 이때, 시리얼라이저를 사용합니다.
    requestValidator = RegisterAirScheduleSerializer(data=request.data)
    # 만약 요청형식에 맞지않는다면 해당 에러를 반환합니다.
    # 항상 형태검증을 할때는 시리얼라이저.is_valid()를 사용하면 됩니다.
    if requestValidator.is_valid() is False:
        # 레스트프레임워크 형태로 응답을 줄때는 Response 객체에 data와 status 인자에 값을 실어 보내면 됩니다.
        return Response(data={"message": "잘못된 요청형식입니다.", "value": None}, status=status.HTTP_400_BAD_REQUEST)

    # 형태는 만족했지만, 존재하지 않는 유저에 대한 운항스케쥴을 생성하면 안됩니다.
    # 때문에 요청객체에서 userId 필드를 가지고 존재하는 유저인지 검증할 필요가 있습니다.
    userQuerySet = User.objects.filter(id=requestValidator.data["userId"])

    # 존재하지 않는 유저라면 운항스케쥴을 작성하면 안되겠죠?
    if not userQuerySet:
        return Response(data={"message": "존재하지 않는 유저입니다.", "value": None}, status=status.HTTP_404_NOT_FOUND)

    # 형태를 만족했고, 존재하는 유저라면 운항스케쥴을 생성해줍니다
    airSchedule = AirSchedule.objects.create(**requestValidator.data)

    # 생성된 운항스케쥴 객체를 필요한 형태로 시리얼라이징 해주면 됩니다.
    # 이때, 운항스케쥴 객체에 유저정보를 함께 표현해주어야한다거나 가미된 정보를
    # 추가해야할 경우가 생길수 있습니다. 이럴때 시리얼라이저의 능력이 빛을 발합니다.
    # 운항스케쥴에 유저정보를 내포해야한다고 가정하고 중첩시리얼라이저를 적용해보겠습니다.
    # 개연성은 없겠지만 나중에 반드시 사용하실 일이 있기때문에 억지로 엮겠습니다 ㅎㅎ
    airScheduleDetail = AirScheduleDetailSerializer(airSchedule, many=False).data
    return Response(data={"message": "성공적으로 생성되었습니다.", "value": airScheduleDetail}, status=status.HTTP_200_OK)


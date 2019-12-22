from django.shortcuts import render
import json
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import RegisterUserRequestSerializer, UserInfoSerializer, RequestUserInfoSerializer


# Create your views here.

# 유저등록 api(세션개념을 넣지않았습니다)
# 단순히 유저를 등록하는것을 rest api형태로 예제를 보이기위함입니다.
# api_view데코레이터는 함수형뷰 위에 작성해주시면되며,
# 메소드를 제한해주는 역할 및 레스트프레임워크 템플릿 형태의 화면을 렌더링할수 있도록 지원해줍니다.
# 다음 형태는 POST 메소드만 허용한다는 것을 의미합니다.
@api_view(["POST"])
def registerUser(request):
    # 들어온 api 요청이 형식을 만족하는지 검증해야합니다.
    # 이때, 시리얼라이저를 사용합니다.
    requestValidatorSerializer = RegisterUserRequestSerializer(data=request.data)
    # 만약 요청형식에 맞지않는다면 해당 에러를 반환합니다.
    # 항상 형태검증을 할때는 시리얼라이저.is_valid()를 사용하면 됩니다.
    if requestValidatorSerializer.is_valid() is False:
        # 레스트프레임워크 형태로 응답을 줄때는 Response 객체에 data와 status 인자에 값을 실어 보내면 됩니다.
        return Response(data={"message": "잘못된 요청형식입니다.", "value": None}, status=status.HTTP_400_BAD_REQUEST)

    # 형태를 만족했다면 유저정보를 생성해줍니다
    user = User.objects.create(**requestValidatorSerializer.data)

    # 생성된 유저객체를 필요한 형태로 시리얼라이징 해주면 됩니다.
    userInfoSerializerData = UserInfoSerializer(user, many=False).data
    return Response(data={"message": "성공적으로 생성되었습니다.", "value": userInfoSerializerData}, status=status.HTTP_200_OK)


# api_view데코레이터는 함수형뷰 위에 작성해주시면되며,
# 메소드를 제한해주는 역할 및 레스트프레임워크 템플릿 형태의 화면을 렌더링할수 있도록 지원해줍니다.
# 다음 형태는 POST 메소드만 허용한다는 것을 의미합니다.
@api_view(["POST"])
def getUserInfo(request):
    # 유저정보를 get으로 가져올경우 보안적으로 문제가 생길수 있으므로 왠만하면 pk정보는 post로 감싸주는것이 좋습니다.
    # 때문에 위에서 api_view 데코레이터에 POST 메소드만 허용하도록합니다.

    # 마찬가지로 유저정보를 요청하는 api 형태검증을 실시합니다.
    # 항상 data 키워드에 request.data를 실어보내주시면 됩니다.
    requestValidator = RequestUserInfoSerializer(data=request.data)
    # 이는 국룰인데 data 인자에 reqeust.data를 실어보내게되면 항상 is_valid를 호출해줘야합니다.
    # 들어온 데이터의 형태를 검증하는 로직인데 형태에 부합하면 True를, 부합하지않으면 False를 반환합니다.
    if requestValidator.is_valid() is False:
        return Response(data={"message": "잘못된 요청형식입니다.", "value": None}, status=status.HTTP_400_BAD_REQUEST)

    # 요청형식에 부합한다면 해당 유저정보를 반환해주면 되겠죠~
    # 단 요청에 userId 값이 넘어왔기때문에 해당 값으로 유저정보를 쿼리해야합니다.
    # 요청데이터의 userId 필드를 id인자에 넣어 orm 쿼리를 돌려주시면 해당 정보가 나오게 됩니다.
    # 단, 해당 유저정보가 존재하지 않는경우도 분명히 있겠죠?
    # 그렇기때문에 쿼리셋 객체만 일단 가져옵니다.
    userQuerySet = User.objects.filter(id=requestValidator.data["userId"])

    # 유저가 존재하지않는다면 위에서 쿼리한 쿼리셋오브젝트가 비어있을겁니다.
    # 비어있다면 해당하는 api응답을 줘야겠죠?
    if not userQuerySet:
        return Response(data={"message": "존재하지 않는 유저입니다.", "value": None}, status=status.HTTP_404_NOT_FOUND)

    # 위에서 빈쿼리셋 검사를 했기때문에,
    # 쿼리셋이 비어있지 않다는것이 증명되었고,
    # 그렇다면 유저인스턴스를 가져옵시다.
    user = userQuerySet.first()  # 또는 userQuerySet[0] 으로 객체를 가져오시면됩니다.

    # 생성된 유저객체를 필요한 형태로 시리얼라이징 해주면 됩니다.
    userInfoSerializerData = UserInfoSerializer(user, many=False).data
    return Response(data={"message": "찾아낸 유저정보", "value": userInfoSerializerData}, status=status.HTTP_200_OK)

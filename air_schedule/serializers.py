from rest_framework import serializers

from user.models import User
from .models import AirSchedule


# 운항스케쥴 등록요청 검증시리얼라이저
class RegisterAirScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirSchedule
        # 운항스케쥴 등록에 필요한 필드만 나열합니다.
        fields = ("userId",
                  "arrival_time",
                  "departure_time",
                  "navigation_section",
                  "operating_time",
                  "airplane_type")


# 운항스케쥴 상세정보에 표기될 유저정보 시리얼라이저
class AirScheduleDetailUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 운항정보에 표기될 유저관련 정보를 나열합니다.
        # 일단은 이름정도만 넣기로 합시다.
        # 더필요한 필드가있다면 명시해주시면 되요!
        fields = ("name",)


# 운항스케쥴 상세정보 시리얼라이저
class AirScheduleDetailSerializer(serializers.ModelSerializer):
    # 유저정보 필드입니다.
    # User테이블과 AirSchedule테이블이 서로 외래키관계라면
    # userInfo = AirScheduleDetailUserInfoSerializer(many=True) 와 같이 사용하시면 됩니다.
    # 하지만 직접 유저정보를 대입시켜줘야하거나 계산된 값을 넣어줘야하는 경우가
    # 더 많기때문에 다음과같이 SerializerMethodField로 값을 구해서 대입시켜줍니다.
    # 시리얼라이저 메소드필드는 실무에서 굉장히 많이 사용될것이기 때문에
    # 사용방법을 익혀두시는것을 추천합니다.

    # 유저정보 계산함수(method_name 과 함수명이 같아야합니다)
    def getUserInfo(self, instance):
        # 파라미터 instance는 이 시리얼라이저 들어온 객체를 의미합니다.
        # 우리가 접근하고싶은 필드는 여기에 들어온 AirSchedule 인스턴스의
        # userId 필드겠죠?
        # 해당필드로 유저를 쿼리해옵시다.
        # 이미 뷰에서는 유저존재여부를 검증했기때문에 반드시 존재한다고 보면됩니다.
        # 유저객체를 바로 가져옵시다.
        user = User.objects.filter(id=instance.userId).first()
        # 이 유저객체를 위에서 정의한 운항스케쥴 유저정보 시리얼라이저에 넣습니다.
        result = AirScheduleDetailUserInfoSerializer(user, many=False).data
        return result

    # 메소드필드 중요하니 연습많이 해보세요~
    userInfo = serializers.SerializerMethodField(method_name="getUserInfo")

    class Meta:
        model = AirSchedule
        # 운항스케쥴 상세보기에 필요한 필드만 나열합니다.
        # 이때 유저id를 외부에 노출할 필요는 없으므로 해당 필드는 제외합니다.
        # 또한 중첩시리얼라이징 할 필드명을 기입해줍니다.
        fields = (
            "userInfo",  # 메소드필드인 유저정보 필드도 등록해줍시다.
            "arrival_time",
            "departure_time",
            "navigation_section",
            "operating_time",
            "airplane_type",
        )

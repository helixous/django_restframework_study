from rest_framework import serializers
from .models import User


class RegisterUserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 유저 생성에 필요한 필드명만 나열합니다.
        # 이 시리얼라이저는 다음 필드만 검증하게 됩니다.
        fields = ("name", "main_address", "sub_address")


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 응답에 필요한 필드명만 나열합니다.
        # 모든필드를 나열하고 싶다면 "__all__" 을 사용합니다.
        fields = "__all__"


# 유저정보요청 형식검증 시리얼라이저
# 모델시리얼라이저로 작성하기보다 일반시리얼라이저를 상속받아 작성합니다.
# 프로덕션환경에서는 추가적인 값을 더 받지만 예제이므로 간단하게
# userId 필드만 받아서 검증하도록 하겠습니다.
# userId가 UUID 필드임을 명시합니다.
# 실제환경에선 패스워드도 함께받아 검증로직을 넣으면됩니다.
class RequestUserInfoSerializer(serializers.Serializer):
    userId = serializers.UUIDField()

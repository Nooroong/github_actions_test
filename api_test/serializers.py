from rest_framework import serializers
from .models import User


# django 모델 기반일 경우 → ModelSerializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User # 기반 모델

#         # 직렬화/역직렬화할 필드 정의
#         fields = "__all__"   # 모든 필드 포함
#         read_only_fields = ("_id")

class UserSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
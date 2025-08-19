import os
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from dotenv import load_dotenv
from mongoengine.connection import get_db
from rest_framework.decorators import action
from bson.objectid import ObjectId
from bson.errors import InvalidId
import time
import functools

from .serializers import UserSerializer
from .models import User

load_dotenv()

default_db = get_db('default')
resume_collection = default_db['resume']
user_collection = default_db['users']

user_id = ObjectId('68a419b3eadca1de1ba451e2')
# Create your views here.

def calc_time(func):
    # @action이 제대로 동작할 수 있도록 원래 함수 메타데이터 보존
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} takes {end_time-start_time} sec")
        
        return result
    return decorated

class TestViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(
            {
                "name": "user",
                "message": "hello, world",
                "image": os.getenv('img_url'),
            },
            status=status.HTTP_200_OK,
        )

class ResumeViewSet(viewsets.ViewSet):
    
    def list(self, request):
        all_resume = resume_collection.find()
        all_resume = list(all_resume)
        print(all_resume[0])
        for resume in all_resume:
            resume["_id"] = str(resume["_id"])
        response_data = list(all_resume) # cursor → dict

        return Response(
            {
                "data": response_data,
            },
            status=status.HTTP_200_OK,
        )

    
class UserViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return UserSerializer
    
    # 데코레이터는 아래에서 위로 적용된다.
    @calc_time
    @action(detail=True, methods=["GET"])
    def get_by_collection(self, request, pk=None):
        # dict 객체를 얻음
        user = user_collection.find_one({"_id":ObjectId(pk)})

        serialized_data = self.get_serializer(user)
        response_data = serialized_data.data

        return Response(
            {
                "data": response_data,
            },
            status=status.HTTP_200_OK,
        )
    
    @calc_time
    @action(detail=True, methods=["DELETE"])
    def del_by_collection(self, request, pk=None):
        result = user_collection.delete_one({"_id":ObjectId(pk)})
        
        return Response(
            {
                "data": result.deleted_count,
            },
            status=status.HTTP_200_OK,
        )
    
    # 데코레이터는 아래에서 위로 적용된다.
    @calc_time
    @action(detail=True, methods=["GET"])
    def get_by_queryset(self, request, pk=None):
        # first()로 하나만 조회하면 models.User 객체를 얻음
        # 조건없이 모든 데이터를 조회하면 Queryset 객체를 얻음
        user = User.objects(
            _id=ObjectId(pk)
        ).first()

        serialized_data = self.get_serializer(user)
        response_data = serialized_data.data

        return Response(
            {
                "data": response_data,
            },
            status=status.HTTP_200_OK,
        )
    
    @calc_time
    @action(detail=True, methods=["DELETE"])
    def del_by_queryset(self, request, pk=None):
        try:
            obj_id = ObjectId(pk)
        except InvalidId:
            return Response({"error": "Invalid ID"}, status=400)
        
        # MongoEngine 모델에서 id 속성을 통해 _id에 접근하도록 래핑되어있다.
        user = User.objects(id=obj_id).first()

        if user:
            user.delete()

            return Response(
                {},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response({"error": "User does not exist."}, status=400)


        
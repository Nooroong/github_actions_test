from django.db import models
from mongoengine import Document, ObjectIdField, StringField

# Create your models here.
class User(Document):
    meta = {
        'db_alias': 'default',
        'collection': 'users'
    }

    '''
    MongoEngine은 자동으로 _id 필드를 생성한다.
    _id를 직접 정의하면 MongoEngine의 내부 _id 관리가 꼬일 수 있다.
    또한 조건을 줄 때 매핑이 잘못되거나 누락될 수 있다.
    그러므로 _id 필드를 직접 정의하지 않는다.
    '''
    # _id = ObjectIdField()
    name = StringField()
    email = StringField()
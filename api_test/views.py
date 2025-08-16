import os
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
class TestViewSet(viewsets.ModelViewSet):
    def list(self, request):
        return Response(
            {
                "name": "user",
                "message": "hello, world",
                "image": os.getenv('img_url'),
            },
            status=status.HTTP_200_OK,
        )
    

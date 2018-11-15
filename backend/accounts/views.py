from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers

class UserCreate(APIView):
    """
    Creates the User
    """

    def post(self, request, format='json'):
        return Response('hello')

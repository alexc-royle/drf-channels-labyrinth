from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers

# Create your views here.

class GameCreate(APIView):
    """
    Creates the Game
    """
    def post(self, request, format='json'):
        requestData = request.data
        requestData['creator'] = request.user.id
        serializer = serializers.GameSerializer(data=requestData)
        if serializer.is_valid():
            game = serializer.save()
            if game:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

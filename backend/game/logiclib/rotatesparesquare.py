from datetime import datetime
from django.db.models import Q, F, Func, ExpressionWrapper, FloatField, Case, When
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response

from .. import serializers
from accounts.serializers import UserSerializer
from .. import models

from math import ceil
from random import sample

class RotateSpareSquare:
    def __init__(self, pk):
        self.pk = pk

    def process(self):
        return self.rotate()

    def rotate(self):
        sparesquare = models.GamePiece.objects.filter(game_id=self.pk, order__isnull=True).select_related('orientation__shape')[0]
        orientations = models.GamePieceOrientation.objects.filter(
            Q(shape_id=sparesquare.orientation.shape.id),
            Q(order=sparesquare.orientation.order+1) | Q(order=1)
        ).order_by('-order')
        sparesquare.orientation = orientations[0]
        sparesquare.save()
        serializer = serializers.GamePieceSerializer(sparesquare, many=False)
        return Response(serializer.data)

from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from . import serializers
from accounts.serializers import UserSerializer
from . import models


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer

    @detail_route(methods=['get'])
    def pieces(self, request, pk=None):
        pieces = models.GamePiece.objects.filter(game_id=pk).order_by('order')
        serializer = serializers.GamePieceSerializer(pieces, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def userCounters(self, request, pk=None):
        userCounters = models.UserCounter.objects.filter(game_id=pk)
        serializer = serializers.UserCounterSerializer(userCounters, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def rotatesparesquare(self, request, pk=None):
        sparesquare = models.GamePiece.objects.get(game_id=pk, order__isnull=True)
        orientations = models.GamePieceOrientation.objects.filter(
            Q(shape_id=sparesquare.orientation.shape.id),
            Q(order=sparesquare.orientation.order+1) | Q(order=1)
        ).order_by('-order')
        sparesquare.orientation = orientations[0]
        sparesquare.save()
        serializer = serializers.GamePieceSerializer(sparesquare, many=False)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def insertsparesquare(self, request, pk=None):
        pieces = models.GamePiece.objects.annotate(
            ordermod=F('order')%7
        ).filter(
            Q(ordermod=2),
            Q(game_id=pk)
        ).order_by('order')
        serializer = serializers.GamePieceSerializer(pieces, many=True)
        return Response(serializer.data)

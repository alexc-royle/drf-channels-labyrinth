from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import serializers
from . import models
from . import logic
from . import pagination

class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    pagination_class = pagination.CustomResultsSetPagination

    @action(detail=True, methods=['get', 'post', 'delete'])
    def player(self, request, pk=None):
        if request.method == 'DELETE':
            return self.player_delete(request, pk)
        elif request.method == 'POST':
            return self.player_add(request, pk)
        return self.player_list(request, pk)

    def player_add(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.LOBBY)
        player = models.Player.objects.filter(game_id=pk, user=request.user)
        if not player:
            new_player = models.Player()
            new_player.game = game
            new_player.user = request.user
            new_player.save()
            serializer = serializers.PlayerSerializer(new_player)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError({ 'detail': 'already registered'})

    def player_delete(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.LOBBY)
        player = models.Player.objects.filter(game_id=pk, user=request.user)
        if player:
            player.delete()
            content = {'detail': 'deleted'}
            return Response({}, status=status.HTTP_200_OK)
        raise ValidationError({ 'detail': 'not registered'})


    def player_list(self, request, pk=None):
        game = self.get_game_or_error(pk)
        players = models.Player.objects.filter(game_id=pk)
        serializer = serializers.PlayerSerializer(players, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.LOBBY)
        player = self.get_request_user_is_game_player_or_400(request, game)
        players = models.Player.objects.filter(game_id=pk)
        if players:
            helper = logic.Start(game, players)
            helper.process()
            serializer = serializers.GameSerializer(game)
            return Response(serializer.data)
        raise ValidationError({ 'detail': 'no players'})

    @action(detail=True, methods=['get'])
    def pieces(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.LOBBY, False)
        pieces = models.GamePiece.objects.filter(game_id=pk).order_by('order')
        serializer = serializers.GamePieceSerializer(pieces, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rotatesparesquare(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        self.get_request_user_is_current_player_or_400(request, game)
        helper = logic.RotateSpareSquare(pk)
        return helper.process()

    @action(detail=True, methods=['post'])
    def insertsparesquare(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        current_player = self.get_request_user_is_current_player_or_400(request, game)
        insert_into = request.data.get('insert_into', False)
        insert_at = request.data.get('insert_at', False)
        helper = logic.InsertSpareSquare(game, current_player, insert_into, insert_at)
        helper.process()
        game_pieces = models.GamePiece.objects.filter(game_id=pk).order_by('order')
        serializer = serializers.GamePieceSerializer(game_pieces, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def collectableitems(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        items = models.CollectableItem.objects.filter(gamepiece__game_id = pk)
        serializer = serializers.CollectableItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def finishturn(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        current_player = self.get_request_user_is_current_player_or_400(request, game)
        helper = logic.FinishTurn(game, current_player)
        helper.process()
        players = models.Player.objects.filter(game_id = pk)
        serializer = serializers.PlayerSerializer(players, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def movecounter(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        player = self.get_request_user_is_current_player_or_400(request, game)
        helper = logic.MoveCounter(request, pk, player)
        helper.process()
        serializer = serializers.PlayerSerializer(player, many=False)
        return Response({ 'data': serializer.data })


    def get_game_or_error(self, pk, status=None, is_equal=True):
        game = get_object_or_404(models.Game, pk=pk)
        if status == None:
            return game
        if is_equal and game.status == status:
            return game
        elif not is_equal and game.status != status:
            return game
        else:
            raise ValidationError({ 'detail': 'operation not allowed on game at this time.'})

    def get_request_user_is_current_player_or_400(self, request, game):
        if game.current_player.user == request.user:
            return game.current_player
        else:
            raise ValidationError({ 'detail': 'not current player' })

    def get_request_user_is_game_player_or_400(self, request, game):
        player = models.Player.objects.filter(game_id=game.id, user_id=request.user.id)
        if not player:
            raise ValidationError({ 'detail': 'not a player of the given game' })
        return player

class ShapeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.GamePieceShape.objects.all()
    serializer_class = serializers.GamePieceShapeSerializer
    pagination_class = None

class OrientationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.GamePieceOrientation.objects.all()
    serializer_class = serializers.GamePieceOrientationSerializer
    pagination_class = None

class CollectableItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CollectableItem.objects.all()
    serializer_class = serializers.CollectableItemSerializer

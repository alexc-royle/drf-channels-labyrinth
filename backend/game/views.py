from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import serializers
from . import models
from . import viewhelpers

class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer


    @detail_route(methods=['get', 'post', 'delete'])
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

    @detail_route(methods=['post'])
    def start(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.LOBBY)
        players = models.Player.objects.filter(game_id=pk)
        if players:
            viewhelpers.Start(game, players)
            serializer = serializers.GameSerializer(game)
            return Response(serializer.data)
        raise ValidationError({ 'detail': 'no players'})

    @detail_route(methods=['get'])
    def pieces(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.LOBBY, False)
        pieces = models.GamePiece.objects.filter(game_id=pk).order_by('order')
        serializer = serializers.GamePieceSerializer(pieces, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def rotatesparesquare(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        self.get_request_user_is_current_player_or_400(request, game)
        helper = viewhelpers.RotateSpareSquare(pk)
        return helper.response

    @detail_route(methods=['post'])
    def insertsparesquare(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        current_player = self.get_request_user_is_current_player_or_400(request, game)
        insert_into = request.POST['insert_into']
        insert_at = request.POST['insert_at']
        viewhelpers.InsertSpareSquare(game, current_player, insert_into, insert_at)
        game_pieces = models.GamePiece.objects.filter(game_id=pk).order_by('order')
        serializer = serializers.GamePieceSerializer(game_pieces, many=True)
        return Response(serializer.data)


    @detail_route(methods=['get'])
    def collectableitems(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        items = models.CollectableItem.objects.filter(gamepiece__game_id = pk)
        serializer = serializers.CollectableItemSerializer(items, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def finishturn(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        current_player = self.get_request_user_is_current_player_or_400(request, game)
        viewhelpers.FinishTurn(game, current_player)
        players = models.Player.objects.filter(game_id = pk)
        serializer = serializers.PlayerSerializer(players, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def movecounter(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        player = self.get_request_user_is_current_player_or_400(request, game)
        viewhelpers.MoveCounter(request, pk, player)
        serializer = serializers.PlayerSerializer(player, many=False)
        return Response(serializer.data)


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

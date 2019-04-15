from django.db.models import Q, F, Func, ExpressionWrapper, FloatField, Case, When
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response

from . import serializers
from accounts.serializers import UserSerializer
from . import models

from math import ceil
from random import sample

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
            # game.status = models.Game.INPROGRESS
            # game.save()
            num_players = len(players)
            order_sequence = sample(list(range(1, num_players + 1)), num_players)
            starting_positions = sample(models.Player.STARTING_POSITION_LIST, 4)
            preserved = Case(*[When(order=order, then=pos) for pos, order in enumerate(starting_positions)])
            game_pieces = models.GamePiece.objects.filter(game_id=pk, order__in=starting_positions).order_by(preserved)
            collectable_items = models.CollectableItem.objects.filter(gamepiece__game_id = pk)
            collectable_items_sequence = sample(list(range(24)), 24)
            items_per_player = 24 / num_players
            player_items = []
            currentIter = 0
            for player in players:
                order = order_sequence.pop(0)
                player.order = order
                player.starting_position = starting_positions.pop(0)
                player.game_piece = game_pieces[currentIter]
                player.starting_game_piece = game_pieces[currentIter]
                player.save()
                if order == 1:
                    game.current_player = player
                collectable_iter = 0
                while collectable_iter < items_per_player:
                    player_item = models.PlayerCollectableItem()
                    player_item.player = player
                    player_item.collectable_item = collectable_items[collectable_items_sequence.pop(0)]
                    player_item.order  = collectable_iter + 1
                    player_items.append(player_item)
                    collectable_iter = collectable_iter + 1
                currentIter = currentIter + 1
            models.PlayerCollectableItem.objects.bulk_create(player_items)
            game.status = models.Game.INPROGRESS
            game.save()
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
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        self.get_request_user_is_current_player_or_400(request, game)
        insert_into = request.POST['insert_into']
        insert_at = request.POST['insert_at']
        if self.validate_insert_spare_square(insert_into, insert_at):
            insert_at = int(insert_at)
            if insert_into in ['top', 'bottom']:
                pieces = self.get_pieces_by_column(pk, insert_at)
            else:
                pieces = self.get_pieces_by_row(pk, insert_at)
            order_by = 'order'
            if insert_into in ['bottom', 'right']:
                order_by = '-order'
            pieces = pieces.order_by(order_by)
            sparesquare = models.GamePiece.objects.get(game_id=pk, order__isnull=True)
            order_numbers = []
            for piece in pieces:
                order_numbers.append(piece.order)
            order_numbers.append(None)
            sparesquare.order = order_numbers.pop(0)
            sparesquare.save()
            for piece in pieces:
                piece.order = order_numbers.pop(0)
                piece.save()
            game_pieces = models.GamePiece.objects.filter(game_id=pk).order_by('order')
            serializer = serializers.GamePieceSerializer(game_pieces, many=True)
            return Response(serializer.data)

    def validate_insert_spare_square(self, insert_into, insert_at):
        if insert_into in ['top', 'bottom', 'left', 'right']:
            insert_at_num = int(insert_at)
            if insert_at_num % 2 == 0:
                return True
        return False

    def get_pieces_by_column(self, pk, column_number):
        return models.GamePiece.objects.annotate(
            ordermod=F('order') % 7
        ).filter(
            Q(ordermod=column_number),
            Q(game_id=pk)
        )

    def get_pieces_by_row(self, pk, row_number):
        minimum = (row_number - 1) * 7 + 1
        maximum = row_number * 7
        return models.GamePiece.objects.filter(
            Q(order__range=(minimum, maximum)),
            Q(game_id=pk)
        )

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
        FinishTurnHelper(game, current_player)
        players = models.Player.objects.filter(game_id = pk)
        serializer = serializers.PlayerSerializer(players, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def movecounter(self, request, pk=None):
        game = self.get_game_or_error(pk, models.Game.INPROGRESS)
        player = self.get_request_user_is_current_player_or_400(request, game)
        MoveCounterHelper(request, pk, player)
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

class FinishTurnHelper:
    def __init__(self, game, current_player):
        self.game = game
        self.player = current_player
        self.check_if_completed()
        if self.game.status != models.Game.COMPLETED:
            self.set_current_player()

    def check_if_completed(self):
        if self.player.remaining_item_count() == 0 and self.player.on_starting_square():
            self.player.completed = True
            self.player.save()
            game_changed = False
            if not self.game.winner:
                self.game.winner = self.player
                game_changed = True
            if self.should_continue():
                self.game.status = models.Game.COMPLETED
                game_changed = True
            if game_changed:
                self.game.save()

    def should_continue(self):
        all_player_count = models.Player.objects.filter(game_id = self.game.id).count()
        completed_count = models.Player.objects.filter(game_id = self.game.id, completed = True).count()
        if all_player_count > 1 and all_player_count - completed_count == 1:
            return False
        elif all_player_count == completed_count:
            return False
        return True

    def set_current_player(self):
        next_player = models.Player.objects.filter(
            Q(game_id = self.game.id),
            Q(completed = False),
            Q(order__gte = self.player.order + 1) | Q(order__gte = 1)
        ).order_by('-order').first()
        if next_player:
            game.current_player = next_player
            game.save()

class MoveCounterHelper:
    def __init__(self, request, pk, player):
        self.movex = self.parse_input(request.data['movex'])
        self.movey = self.parse_input(request.data['movey'])
        self.value_changed = self.get_changed(self.movex, self.movey)
        self.game_pk = pk
        self.player = player
        self.old_position = player.game_piece.order
        self.new_position_data = self.get_new_position_data()
        self.update_position()


    def parse_input(self, input):
        possible_values = [-1, 0, 1]
        try:
            if int(input) in possible_values:
                return int(input)
            else:
                raise ValidationError({ 'detail': 'only integers in the range -1, 0 and 1 are accepted'})
        except ValueError:
            raise ValidationError({ 'detail': 'only integers in the range -1, 0 and 1 are accepted'})

    def get_changed(self, movex, movey):
        if movex == 0 and movey == 0:
            raise ValidationError({ 'detail': 'you can\'t just stay in the same place'})
        elif movex != 0 and movey != 0:
            raise ValidationError({ 'detail': 'you can\'t move diagonally'})
        elif movex == 0:
            return 'movey'
        else:
            return 'movex'

    def get_new_position_data(self):
        if self.value_changed == 'movex':
            return self.get_new_position_x()
        else:
            return self.get_new_position_y()

    def get_new_position_x(self):
        self.within_bounds_x()
        new_position = self.old_position + self.movex
        if new_position > self.old_position:
            return (new_position, 'right', 'left')
        else:
            return (new_position, 'left', 'right')

    def within_bounds_x(self):
        mod_current = self.old_position % 7
        if (mod_current == 1 and self.movex == -1) or (mod_current == 0 and self.movex == 1):
            raise ValidationError({ 'detail': 'out of bounds' })

    def get_new_position_y(self):
        self.within_bounds_y()
        new_position = self.old_position + (self.movey * 7)
        if new_position > self.old_position:
            return (new_position, 'down', 'up')
        else:
            return (new_position, 'up', 'down')

    def within_bounds_y(self, current_position, movey):
        new_position = current_position + (movey * 7)
        if (new_position < 1) or (new_position > 49):
            raise ValidationError({ 'detail': 'out of bounds' })

    def update_position(self):
        (new_position, move_from, move_to) = self.new_position_data
        old_gamepiece = self.player.game_piece
        new_gamepiece = models.GamePiece.objects.filter(game_id=self.game_pk, order=new_position)[0]
        if old_gamepiece.orientation[move_from] and new_gamepiece.orientation[move_to]:
            self.player.game_piece = new_gamepiece
            self.player.save()
        else:
            raise ValidationError({ 'detail': 'player cannot move in that direction' })

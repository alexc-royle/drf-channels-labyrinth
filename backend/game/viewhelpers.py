from datetime import datetime
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

class Start:
    def __init__(self, game, players):
        self.game = game
        self.players = players
        self.num_players = len(players)
        self.order_sequence = sample(list(range(1, self.num_players + 1)), self.num_players)
        self.starting_positions = sample(models.Player.STARTING_POSITION_LIST, 4)
        self.game_pieces = self.get_game_pieces()
        self.collectable_items = models.CollectableItem.objects.filter(gamepiece__game_id = self.game.id)
        self.collectable_items_sequence = sample(list(range(24)), 24)
        self.items_per_player = 24 / self.num_players
        self.player_items = []
        self.process_players()
        models.PlayerCollectableItem.objects.bulk_create(self.player_items)
        self.game.status = models.Game.INPROGRESS
        self.game.save()

    def get_game_pieces(self):
        preserved = Case(*[When(order=order, then=pos) for pos, order in enumerate(self.starting_positions)])
        return models.GamePiece.objects.filter(game_id=self.game.id, order__in=self.starting_positions).order_by(preserved)

    def process_players(self):
        currentIter = 0
        for player in self.players:
            player.order = self.order_sequence.pop(0)
            player.starting_position = self.starting_positions.pop(0)
            player.game_piece = self.game_pieces[currentIter]
            player.starting_game_piece = self.game_pieces[currentIter]
            player.save()
            if player.order == 1:
                self.game.current_player = player
            self.process_collectables(player)
            currentIter = currentIter + 1

    def process_collectables(self, player):
        collectable_iter = 0
        while collectable_iter < self.items_per_player:
            player_item = models.PlayerCollectableItem()
            player_item.player = player
            player_item.collectable_item = self.collectable_items[self.collectable_items_sequence.pop(0)]
            player_item.order  = collectable_iter + 1
            self.player_items.append(player_item)
            collectable_iter = collectable_iter + 1


class RotateSpareSquare:
    def __init__(self, pk):
        self.pk = pk
        self.response = self.rotate()

    def rotate(self):
        sparesquare = models.GamePiece.objects.get(game_id=pk, order__isnull=True)
        orientations = models.GamePieceOrientation.objects.filter(
            Q(shape_id=sparesquare.orientation.shape.id),
            Q(order=sparesquare.orientation.order+1) | Q(order=1)
        ).order_by('-order')
        sparesquare.orientation = orientations[0]
        sparesquare.save()
        serializer = serializers.GamePieceSerializer(sparesquare, many=False)
        return Response(serializer.data)

class InsertSpareSquare:
    def __init__(self, game, current_player, insert_into, insert_at):
        self.game = game
        self.player = current_player
        self.insert_into = insert_into
        self.insert_at = insert_at
        self.validate()
        self.insert_spare_square()

    def validate(self):
        if not self.insert_into in ['top', 'bottom', 'left', 'right']:
            raise ValidationError({ 'detail': 'unknown insert into value given'})
        try:
            insert_at_num = int(insert_at)
            if insert_at_num % 2 == 0:
                self.insert_at = insert_at_num
            else:
                raise ValidationError({ 'detail': 'unknown insert at value given'})
        except ValueError:
            raise ValidationError({ 'detail': 'unknown insert at value given'})

    def insert_spare_square(self):
        pieces = self.get_pieces()
        order_by = self.get_order()
        pieces.order_by(order_by)
        sparesquare = models.GamePiece.objects.get(game_id=pk, order__isnull=True)
        order_numbers = self.get_order_numbers(pieces)
        self.update_orders(sparesquare, pieces, order_numbers)

    def get_pieces(self):
        if self.insert_into in ['top', 'bottom']:
            pieces = self.get_pieces_by_column()
        else:
            pieces = self.get_pieces_by_row()
        return pieces

    def get_pieces_by_column(self):
        return models.GamePiece.objects.annotate(
            ordermod=F('order') % 7
        ).filter(
            Q(ordermod=self.insert_at),
            Q(game_id=self.game.id)
        )

    def get_pieces_by_row(self):
        minimum = (self.insert_at - 1) * 7 + 1
        maximum = self.insert_at * 7
        return models.GamePiece.objects.filter(
            Q(order__range=(minimum, maximum)),
            Q(game_id=self.game.id)
        )

    def get_order(self):
        if self.insert_into in ['bottom', 'right']:
            return '-order'
        return  'order'

    def get_order_numbers(self, pieces):
        order_numbers = []
        for piece in pieces:
            order_numbers.append(piece.order)
        order_numbers.append(None)
        return order_numbers

    def update_orders(self, sparesquare, pieces, order_numbers):
        sparesquare.order = order_numbers.pop(0)
        sparesquare.save()
        for piece in pieces:
            piece.order = order_numbers.pop(0)
            piece.save()

class FinishTurn:
    def __init__(self, game, current_player):
        self.game = game
        self.player = current_player
        self.check_if_completed()
        if self.game.status != models.Game.COMPLETED:
            self.set_current_player()

    def check_if_completed(self):
        game_changed = False
        player_changed = False
        if self.player.remaining_item_count() == 0 and self.player.on_starting_square():
            self.player.completed_time = datetime.now()
            self.player.save()
            if not self.game.winner:
                self.game.winner = self.player
                game_changed = True
            if not self.should_continue():
                self.game.status = models.Game.COMPLETED
                game_changed = True
            if game_changed:
                self.game.save()

    def should_continue(self):
        all_player_count = models.Player.objects.filter(game_id = self.game.id).count()
        completed_count = models.Player.objects.filter(game_id = self.game.id).exclude(completed_time = None).count()
        if all_player_count > 1 and all_player_count - completed_count == 1:
            return False
        elif all_player_count == completed_count:
            return False
        return True

    def set_current_player(self):
        next_player = models.Player.objects.filter(
            Q(game_id = self.game.id),
            Q(completed_time = None),
            Q(order__gt = self.player.order) | Q(order__gte = 1)
        ).order_by('-order').first()
        if next_player:
            self.game.current_player = next_player
            self.game.save()

class MoveCounter:
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

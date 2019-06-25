from datetime import datetime
from django.db.models import Q, F, Func, ExpressionWrapper, FloatField, Case, When
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response

from .. import serializers
from accounts.serializers import UserSerializer
from .. import models

from math import ceil
from random import sample

class InsertSpareSquare:
    def __init__(self, game, current_player, insert_into, insert_at):
        self.game = game
        self.player = current_player
        self.insert_into = insert_into
        self.insert_at = insert_at
        self.turn = models.PlayerTurn.objects.filter(player_id=self.player.id).order_by('-id').first()

    def process(self):
        self.check_turn()
        self.validate()
        self.convert_insert_at()
        self.check_previous_turn()
        self.insert_spare_square()

    def check_turn(self):
        if self.turn.turn_status != models.PlayerTurn.PRE_INSERT_SPARESQUARE:
            raise ValidationError({ 'detail': 'player has already inserted a spare square this turn'})

    def validate(self):
        if not self.insert_into or not self.insert_at:
            raise ValidationError({ 'detail': 'missing required values'})
        if not self.insert_into in ['top', 'bottom', 'left', 'right']:
            raise ValidationError({ 'detail': 'unknown insert into value given'})
        if not self.insert_at in [2, 4, 6, '2', '4', '6']:
            raise ValidationError({ 'detail': 'invalid insert_at value given'})

    def convert_insert_at(self):
        try:
            self.insert_at = int(self.insert_at)
        except ValueError:
            raise ValidationError({ 'detail': 'invalid insert at value given'})

    def check_previous_turn(self):
        previous_turn = models.PlayerTurn.objects.filter(player__game_id=self.game.id).order_by('-id')[1]
        if previous_turn:
            if self.insert_at == previous_turn.spare_square_inserted_at:
                dir_map = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}
                if dir_map[self.insert_into] == previous_turn.spare_square_inserted_into:
                    raise ValidationError({ 'detail': 'cannot undo the change the previous player made'})

    def insert_spare_square(self):
        pieces = self.get_pieces()
        order_by = self.get_order()
        pieces = pieces.order_by(order_by)
        sparesquare = models.GamePiece.objects.get(game_id=self.game.id, order__isnull=True)
        order_numbers = self.get_order_numbers(pieces)
        self.update_orders(sparesquare, pieces, order_numbers)
        self.update_turn()

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

    def update_turn(self):
        self.turn.turn_status = models.PlayerTurn.POST_INSERT_SPARESQUARE
        self.turn.spare_square_inserted_into = self.insert_into
        self.turn.spare_square_inserted_at = self.insert_at
        self.turn.save()

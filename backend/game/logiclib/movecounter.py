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

class MoveCounter:
    def __init__(self, request, pk, player):
        self.game_pk = pk
        self.player = player
        self.movex = self.parse_input(request.data['movex'])
        self.movey = self.parse_input(request.data['movey'])

    def process(self):
        self.value_changed = self.get_changed(self.movex, self.movey)
        self.old_position = self.player.game_piece.order
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

    def within_bounds_y(self):
        new_position = self.old_position + (self.movey * 7)
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

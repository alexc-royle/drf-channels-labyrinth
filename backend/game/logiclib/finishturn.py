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

class FinishTurn:
    def __init__(self, game, current_player):
        self.game = game
        self.player = current_player

    def process(self):
        if not self.check_if_completed():
            self.check_player_on_collectable()
        if self.game.status != models.Game.COMPLETED:
            self.set_current_player()

    def check_if_completed(self):
        game_changed = False
        player_changed = False
        if self.player.remaining_collectable_item_count() == 0 and self.player.on_starting_square():
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
            return True
        return False

    def check_player_on_collectable(self):
        if self.player.on_next_collectable_item():
            next_item = self.player.next_collectable_item()
            next_item.playercollectableitem.collected = True
            next_item.playercollectableitem.save()

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
            Q(order__gt = self.player.order)
        ).order_by('order').first()
        if not next_player:
            next_player = models.Player.objects.filter(
                Q(game_id = self.game.id),
                Q(completed_time = None),
                Q(order__gte = 1)
            ).order_by('order').first()
        if next_player:
            self.game.current_player = next_player
            self.game.save()

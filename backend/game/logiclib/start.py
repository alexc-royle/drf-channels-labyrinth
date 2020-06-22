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

class Start:
    def __init__(self, game, players):
        self.game = game
        self.players = players

    def process(self):
        self.num_players = len(self.players)
        self.order_sequence = self.get_order_sequence()
        self.starting_positions = self.get_starting_positions()
        self.game_pieces = self.get_game_pieces()
        self.collectable_items = list(models.CollectableItem.objects.filter(gamepiece__game_id = self.game.id))
        self.collectable_items_sequence = self.get_collectable_items_sequence()
        self.items_per_player = 24 / self.num_players
        self.player_items = []
        self.process_players()
        models.PlayerCollectableItem.objects.bulk_create(self.player_items)
        self.game.status = models.Game.INPROGRESS
        self.game.save()

    def get_order_sequence(self):
        return sample(list(range(1, self.num_players + 1)), self.num_players)

    def get_starting_positions(self):
        return sample(models.Player.STARTING_POSITION_LIST, 4)

    def get_game_pieces(self):
        preserved = Case(*[When(order=order, then=pos) for pos, order in enumerate(self.starting_positions)])
        return models.GamePiece.objects.filter(game_id=self.game.id, order__in=self.starting_positions).order_by(preserved)

    def get_collectable_items_sequence(self):
        return sample(list(range(24)), 24)

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
                self.create_turn(player)

            self.process_collectables(player)
            currentIter = currentIter + 1

    def create_turn(self, player):
        player_turn = models.PlayerTurn()
        player_turn.player = player
        player_turn.save()

    def process_collectables(self, player):
        collectable_iter = 0
        while collectable_iter < self.items_per_player:
            player_item = models.PlayerCollectableItem()
            player_item.player = player
            player_item.collectable_item = self.collectable_items[self.collectable_items_sequence.pop(0)]
            player_item.order  = collectable_iter + 1
            self.player_items.append(player_item)
            collectable_iter = collectable_iter + 1

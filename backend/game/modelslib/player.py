from django.contrib.auth.models import User
from django.db import models

from game.modelslib.collectableitem import *

# Create your models here.

class Player(models.Model):
    game = models.ForeignKey(
        'Game',
        on_delete = models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    game_piece = models.ForeignKey(
        'GamePiece',
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name = 'currentcounters'
    )
    starting_game_piece = models.ForeignKey(
        'GamePiece',
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name = 'startcounters'
    )
    completed_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    order = models.IntegerField(
        null=True,
        blank=True
    )
    TOPLEFT = 1
    TOPRIGHT = 7
    BOTTOMLEFT = 43
    BOTTOMRIGHT = 49
    STARTING_POSITION_LIST = [
        TOPLEFT,
        TOPRIGHT,
        BOTTOMLEFT,
        BOTTOMRIGHT
    ]
    STARTING_POSITION_CHOICES = (
        (TOPLEFT, 'top_left'),
        (TOPRIGHT, 'top_right'),
        (BOTTOMLEFT, 'bottom_left'),
        (BOTTOMRIGHT, 'bottom_right')
    )
    starting_position = models.IntegerField(
        choices = STARTING_POSITION_CHOICES,
        null = True,
        blank=True
    )

    def remaining_collectable_item_count(self):
        return CollectableItem.objects.filter(
            playercollectableitem__player_id = self.id,
            playercollectableitem__collected = False
        ).count()

    def next_collectable_item(self):
        return CollectableItem.objects.filter(playercollectableitem__player_id = self.id,
            playercollectableitem__collected = False
        ).order_by('playercollectableitem__order').first()

    def next_collectable_item_id(self):
        next_item = self.next_collectable_item()
        if next_item:
            return next_item.id
        return None

    def on_starting_square(self):
        return self.game_piece == self.starting_game_piece

    def current_turn(self):
        return (self == self.game.current_player)

    def on_next_collectable_item(self):
        next_item = self.next_collectable_item()
        return self.game_piece.collectable_item == next_item

    def completed(self):
        return (self.completed_time != None or self.game.status == models.Game.COMPLETED)

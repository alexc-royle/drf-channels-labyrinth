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

    def remaining_item_count(self):
        return CollectableItem.objects.filter(
            playercollectableitem__player_id = self.id,
            playercollectableitem__collected = False
        ).count()

    def on_starting_square(self):
        return self.game_piece == self.starting_game_piece

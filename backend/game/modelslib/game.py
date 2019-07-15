from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import sample, choice

from game.modelslib.basegamepiece import *
from game.modelslib.collectableitem import *
from game.modelslib.gamepieceorientation import *
from game.modelslib.gamepiece import *
from game.modelslib.player import *
from .. import decorators

# Create your models here.

class Game(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null=True
    )
    current_player = models.ForeignKey(
        'Player',
        on_delete = models.CASCADE,
        null = True,
        related_name = 'currentplayer'
    )
    winner = models.ForeignKey(
        'Player',
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'winningplayer'
    )
    LOBBY = 1
    INPROGRESS = 2
    COMPLETED = 3
    GAME_STATUS_CHOICES = (
        (LOBBY, 'lobby'),
        (INPROGRESS, 'in_progress'),
        (COMPLETED, 'completed')
    )
    status = models.IntegerField(
        choices = GAME_STATUS_CHOICES,
        default = LOBBY
    )

@decorators.suspendingreceiver(post_save, sender=Game)
def create_game_pieces(sender, instance=None, created=False, raw=False, **kwargs):
    if created and not raw:
        game_pieces = []
        available_piece_order = sample(list(range(1, 51)), 50)
        orientations_by_shape = {}
        base_game_pieces = BaseGamePiece.objects.all().order_by('order').prefetch_related('orientation', 'shape')
        collectable_items = CollectableItem.objects.all()
        collectable_items_count = len(collectable_items)
        available_image_order = sample(list(range(collectable_items_count)), 24)

        for base_game_piece in base_game_pieces:
            if base_game_piece.order:
                available_piece_order.remove(base_game_piece.order)

        for base_game_piece in base_game_pieces:
            if not base_game_piece.shape.title in orientations_by_shape.keys():
                orientations_by_shape[base_game_piece.shape.title] = GamePieceOrientation.objects.filter(shape=base_game_piece.shape)
            for x in range(base_game_piece.number_of_items):
                current_game_piece = GamePiece()
                current_game_piece.game = instance
                if base_game_piece.orientation:
                    current_game_piece.orientation = base_game_piece.orientation
                else:
                    current_game_piece.orientation = choice(orientations_by_shape[base_game_piece.shape.title])
                if base_game_piece.has_image:
                    current_game_piece.collectable_item = collectable_items[available_image_order.pop(0)]
                if base_game_piece.order:
                    current_game_piece.order = base_game_piece.order
                game_pieces.append(current_game_piece)

        random_ordered_game_pieces = sample(game_pieces, len(game_pieces))
        for game_piece in random_ordered_game_pieces:
            if not game_piece.order:
                order = available_piece_order.pop(0)
                if order < 50:
                    game_piece.order = order

        GamePiece.objects.bulk_create(random_ordered_game_pieces)

@decorators.suspendingreceiver(post_save, sender=Game)
def create_user_counter(sender, instance=None, created=False, raw=False, **kwargs):
    if created and not raw:
        user_counter = Player()
        user_counter.game = instance
        user_counter.user = instance.creator
        user_counter.save()

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import sample, choice
# Create your models here.
class GamePieceShape(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class GamePieceOrientation(models.Model):
    shape = models.ForeignKey(
        'GamePieceShape',
        on_delete=models.CASCADE
    )
    order = models.IntegerField(null=True)
    up = models.BooleanField(default=False)
    down = models.BooleanField(default=False)
    left = models.BooleanField(default=False)
    right = models.BooleanField(default=False)

    def __str__(self):
        return '{0.shape} orientation {0.order}'.format(self)

class CollectableItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    class_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class BaseGamePiece(models.Model):
    orientation = models.ForeignKey(
        'GamePieceOrientation',
        on_delete = models.CASCADE,
        blank=True,
        null=True
    )
    shape = models.ForeignKey(
        'GamePieceShape',
        on_delete = models.CASCADE,
        default=1
    )
    has_image = models.BooleanField(default=False)
    order = models.IntegerField(null=True)
    number_of_items = models.IntegerField(default = 1)

class Game(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
@receiver(post_save, sender=Game)
def create_game_pieces(sender, instance=None, created=False, **kwargs):
    if created:
        game_pieces = []
        available_piece_order = sample(list(range(1, 51)), 50)
        orientations_by_shape = {}
        base_game_pieces = BaseGamePiece.objects.all().order_by('order')
        collectable_items = CollectableItem.objects.all()
        collectable_items_count = len(collectable_items)
        available_image_order = sample(list(range(collectable_items_count)), 24)
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
                    available_piece_order.remove(base_game_piece.order)
                else:
                    order = available_piece_order.pop(0)
                    if order < 50:
                        current_game_piece.order = order
                game_pieces.append(current_game_piece)
        GamePiece.objects.bulk_create(game_pieces)


class GamePiece(models.Model):
    game = models.ForeignKey(
        'Game',
        related_name = 'pieces',
        on_delete = models.CASCADE,
    )
    orientation = models.ForeignKey(
        'GamePieceOrientation',
        on_delete = models.CASCADE,
    )
    collectable_item = models.ForeignKey(
        'CollectableItem',
        on_delete = models.CASCADE,
        null=True
    )
    order = models.IntegerField(null=True)

class UserCounter(models.Model):
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
        on_delete = models.CASCADE
    )
    collectable_items = models.ManyToManyField(
        'CollectableItem',
    )

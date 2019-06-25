from django.db import models

# Create your models here.

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

from django.db import models

# Create your models here.

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

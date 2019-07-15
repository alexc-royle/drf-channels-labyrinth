from django.db import models

# Create your models here.

class PlayerCollectableItem(models.Model):
    player = models.ForeignKey(
        'Player',
        on_delete = models.CASCADE
    )
    collectable_item = models.OneToOneField(
        'CollectableItem',
        on_delete = models.CASCADE,
        related_name = 'playercollectableitem',
    )
    order = models.IntegerField()
    collected = models.BooleanField(default=False)

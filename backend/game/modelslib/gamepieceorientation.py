from django.db import models

# Create your models here.

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
    def __getitem__(self, key):
        if key == 'up':
            return self.up
        elif key == 'down':
            return self.down
        elif key == 'left':
            return self.left
        elif key == 'right':
            return self.right
        else:
            return undefined

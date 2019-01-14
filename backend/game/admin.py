from django.contrib import admin

from . import models

admin.site.register(models.GamePieceShape)
admin.site.register(models.GamePieceOrientation)
admin.site.register(models.CollectableItem)
admin.site.register(models.BaseGamePiece)
admin.site.register(models.GamePiece)
admin.site.register(models.Game)

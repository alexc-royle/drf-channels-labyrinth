from django.db import models

# Create your models here.

class PlayerTurn(models.Model):
    player = models.ForeignKey(
        'Player',
        on_delete = models.CASCADE
    )
    PRE_INSERT_SPARESQUARE = 1
    POST_INSERT_SPARESQUARE = 2

    TURN_STATUS_CHOICES = (
        (PRE_INSERT_SPARESQUARE, 'Pre-insert of spare square'),
        (POST_INSERT_SPARESQUARE, 'Post-insert of spare square'),
    )
    turn_status = models.IntegerField(
        choices = TURN_STATUS_CHOICES,
        default = PRE_INSERT_SPARESQUARE
    )
    spare_square_inserted_into = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    spare_square_inserted_at = models.IntegerField(
        null=True,
        blank=True
    )
    def __str__(self):
        return "id: {}, player_id: {}, status: {}, inserted_into: {}, inserted_at: {}".format(
            self.id,
            self.player.id,
            self.turn_status,
            self.spare_square_inserted_into,
            self.spare_square_inserted_at
        )

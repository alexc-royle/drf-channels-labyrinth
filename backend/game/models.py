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

class PlayerCollectableItem(models.Model):
    player = models.ForeignKey(
        'Player',
        on_delete = models.CASCADE
    )
    collectable_item = models.ForeignKey(
        'CollectableItem',
        on_delete = models.CASCADE,
    )
    order = models.IntegerField()
    collected = models.BooleanField(default=False)

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

@receiver(post_save, sender=Game)
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

@receiver(post_save, sender=Game)
def create_user_counter(sender, instance=None, created=False, **kwargs):
    if created:
        user_counter = Player()
        user_counter.game = instance
        user_counter.user = instance.creator
        user_counter.save()

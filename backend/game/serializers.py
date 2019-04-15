from rest_framework import serializers
from . import models

class GamePieceShapeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'title',
        )
        model = models.GamePieceShape

class GamePieceOrientationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'shape', 'order', 'up', 'down', 'left', 'right'
        )
        model = models.GamePieceOrientation

class CollectableItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'title', 'description', 'class_name'
        )
        model = models.CollectableItem

class BaseGamePieceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'title', 'orientation', 'shape', 'has_image', 'order', 'number_of_items'
        )
        model = models.BaseGamePiece

class GamePieceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'game', 'orientation', 'collectable_item', 'order'
        )
        model = models.GamePiece

class GameSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source='get_status_display',
        required = False
    )
    class Meta:
        fields = (
            'id', 'creator', 'current_player', 'status_display'
        )
        model = models.Game

    def create(self, validated_data):
        creator = self.context['request'].user
        return models.Game.objects.create(creator=creator, **validated_data)

class PlayerCollectableItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'player', 'collectable_item', 'order', 'collected'
        )
        model = models.PlayerCollectableItem

class PlayerSerializer(serializers.ModelSerializer):
    current_turn = serializers.SerializerMethodField()
    remaining_collectable_items = serializers.SerializerMethodField()
    next_collectable_item = serializers.SerializerMethodField()
    class Meta:
        fields = (
            'id', 'game', 'user', 'game_piece', 'order', 'starting_position', 'starting_game_piece', 'current_turn', 'remaining_collectable_items', 'next_collectable_item', 'remaining_item_count'
        )
        model = models.Player
    def get_current_turn(self, obj):
        return (obj == obj.game.current_player)
    def get_collectable_items(self, obj):
        return models.CollectableItem.objects.filter(
            playercollectableitem__player_id = obj.id
        ).order_by('playercollectableitem__order').values_list('id', flat=True)
    def get_remaining_collectable_items(self, obj):
        return models.CollectableItem.objects.filter(
            playercollectableitem__player_id = obj.id,
            playercollectableitem__collected = False
        ).count()
    def get_next_collectable_item(self, obj):
        next_item = models.CollectableItem.objects.filter(playercollectableitem__player_id = obj.id,
            playercollectableitem__collected = False
        ).order_by('playercollectableitem__order').first()
        if next_item:
            return next_item.id
        return None

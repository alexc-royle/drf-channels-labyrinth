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
    class Meta:
        fields = (
            'id', 'game', 'user', 'game_piece', 'order', 'starting_position', 'starting_game_piece',
            'current_turn', 'next_collectable_item_id', 'remaining_collectable_item_count', 'completed'
        )
        model = models.Player

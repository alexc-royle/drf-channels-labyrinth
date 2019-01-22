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
    class Meta:
        fields = (
            'id', 'creator'
        )
        model = models.Game
        
    def create(self, validated_data):
        creator = self.context['request'].user
        return models.Game.objects.create(creator=creator, **validated_data)

class UserCounterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'game', 'user', 'game_piece', 'collectable_items'
        )
        model = models.UserCounter

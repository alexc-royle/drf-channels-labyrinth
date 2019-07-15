from django.utils import timezone
from django.test import override_settings
from rest_framework.test import APITestCase, APIClient
from unittest.mock import Mock, patch
from pprint import pprint

from django.dispatch import Signal

from model_mommy import mommy

from .. import models
from .. import logic

# Create your tests here.
@override_settings(SUSPEND_SIGNALS=True)
class MoveCounterTest(APITestCase):
    def setUp(self):
        self.game = mommy.make('game.Game', status=models.Game.INPROGRESS)
        self.players = [
            mommy.make('game.Player', game=self.game, order=1),
            mommy.make('game.Player', game=self.game, order=2, completed_time=timezone.now()),
            mommy.make('game.Player', game=self.game, order=3),
            mommy.make('game.Player', game=self.game, order=4)
        ]
        self.game.current_player = self.players[0]

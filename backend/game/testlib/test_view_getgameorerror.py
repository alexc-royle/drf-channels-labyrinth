from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from .. import models
from .. import views

# Create your tests here.

class GameViewGetGameOrErrorTest(APITestCase):
    fixtures = ['game/fixtures/data.json',]
    def setUp(self):
        first_user = User.objects.create_user('test_user1', 'test1@example.com', 'testpassword')
        self.game = models.Game()
        self.game.creator = first_user
        self.game.save()
        self.view = views.GameViewSet()

    def test_get_existing_game(self):
        game = self.view.get_game_or_error(self.game.id)
        self.assertEqual(game, self.game)

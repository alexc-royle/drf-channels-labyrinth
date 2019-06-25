from django.contrib.auth.models import User
from django.db.models import Case, When, Q, Count, F
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
import json

from .. import models
from .. import views

# Create your tests here

class StartGameTest(APITestCase):
    fixtures = ['game/fixtures/data.json', 'game/fixtures/user.json', 'game/fixtures/start_game_data.json']
    def setUp(self):
        game = models.Game.objects.get(id=1)
        token = Token.objects.get(user_id=1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('game-start', kwargs={'pk': 1})
        self.game = game

    def test_when_logged_in(self):
        response = self.client.post(self.url, {}, format='json')
        game = models.Game.objects.get(id=1)
        players = models.Player.objects.filter(game_id=game.id)
        player = models.Player.objects.filter(game_id=game.id).first()
        player_collectables = models.PlayerCollectableItem.objects.filter(player_id=player.id)
        player_turns = models.PlayerTurn.objects.filter(player_id=player.id)
        player_turn = player_turns.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(game.status, models.Game.INPROGRESS)
        self.assertTrue(players.count() == 1)
        self.assertTrue(game.current_player == player)
        self.assertTrue(player.starting_position in [1, 7, 43, 49])
        self.assertTrue(player.game_piece == player.starting_game_piece)
        self.assertTrue(player.game_piece.order in [1, 7, 43, 49])
        self.assertEqual(player.order, 1)
        self.assertEqual(player_collectables.count(), 24)
        self.assertEqual(player_turns.count(), 1)
        self.assertEqual(player_turn.turn_status, models.PlayerTurn.PRE_INSERT_SPARESQUARE)
        self.assertEqual(player_turn.spare_square_inserted_into, None)
        self.assertEqual(player_turn.spare_square_inserted_at, None)

    def test_when_logged_out(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_when_game_has_started(self):
        self.game.status = models.Game.INPROGRESS
        self.game.save()
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_started_by_non_player(self):
        token = Token.objects.get(user_id=2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_two_players(self):
        self.create_player(2, self.game)
        response = self.client.post(self.url, {}, format='json')
        players = models.Player.objects.filter(game_id=self.game.id)
        player_turns = models.PlayerTurn.objects.all()
        orders = [1, 2]
        starting_positions = [1, 7, 43, 49]
        self.assertEqual(players.count(), 2)
        self.assertEqual(player_turns.count(), 1)
        for player in players:
            player_collectables = models.PlayerCollectableItem.objects.filter(player_id=player.id)
            self.assertEqual(player_collectables.count(), 12)
            self.assertTrue(player.order in orders)
            orders.remove(player.order)
            self.assertTrue(player.starting_position in starting_positions)
            starting_positions.remove(player.starting_position)

    def test_when_three_players(self):
        self.create_player(2, self.game)
        self.create_player(3, self.game)
        response = self.client.post(self.url, {}, format='json')
        players = models.Player.objects.filter(game_id=self.game.id)
        player_turns = models.PlayerTurn.objects.all()
        orders = [1, 2, 3]
        starting_positions = [1, 7, 43, 49]
        self.assertEqual(players.count(), 3)
        self.assertEqual(player_turns.count(), 1)
        for player in players:
            player_collectables = models.PlayerCollectableItem.objects.filter(player_id=player.id)
            self.assertEqual(player_collectables.count(), 8)
            self.assertTrue(player.order in orders)
            orders.remove(player.order)
            self.assertTrue(player.starting_position in starting_positions)
            starting_positions.remove(player.starting_position)

    def test_when_four_players(self):
        self.create_player(2, self.game)
        self.create_player(3, self.game)
        self.create_player(4, self.game)
        response = self.client.post(self.url, {}, format='json')
        players = models.Player.objects.filter(game_id=self.game.id)
        player_turns = models.PlayerTurn.objects.all()
        orders = [1, 2, 3, 4]
        starting_positions = [1, 7, 43, 49]
        self.assertEqual(players.count(), 4)
        self.assertEqual(player_turns.count(), 1)
        for player in players:
            player_collectables = models.PlayerCollectableItem.objects.filter(player_id=player.id)
            self.assertEqual(player_collectables.count(), 6)
            self.assertTrue(player.order in orders)
            orders.remove(player.order)
            self.assertTrue(player.starting_position in starting_positions)
            starting_positions.remove(player.starting_position)


    def create_player(self, userid, game):
        user = User.objects.get(id=userid)
        player = models.Player()
        player.game = game
        player.user = user
        player.save()
        return player

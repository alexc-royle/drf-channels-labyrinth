from django.contrib.auth.models import User
from django.db.models import Case, When, Q, Count, F
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
import json

from .. import models
from .. import views

# Create your tests here.

class InsertSpareSquareTest(APITestCase):
    fixtures = ['game/fixtures/data.json', 'game/fixtures/user.json', 'game/fixtures/game.json']
    def setUp(self):
        game = models.Game.objects.get(id=1)
        token = Token.objects.get(user_id=1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('game-insertsparesquare', kwargs={'pk': 1})
        self.game = game

    def test_when_logged_in(self):
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_when_logged_out(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_when_no_data_sent(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_insert_at_not_number(self):
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 'aaa'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_insert_at_is_odd(self):
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_insert_at_less_than_two(self):
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_insert_at_greater_than_six(self):
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 8}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_insert_into_not_recognised(self):
        response = self.client.post(self.url, {'insert_into': 'boo', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_game_in_lobby(self):
        self.game.status = models.Game.LOBBY
        self.game.save()
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_game_is_completed(self):
        self.game.status = models.Game.COMPLETED
        self.game.save()
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_not_user_turn(self):
        token = Token.objects.get(user_id=2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_multiple_calls_in_same_turn(self):
        self.client.post(self.url, {'insert_into': 'top', 'insert_at': 2}, format='json')
        response = self.client.post(self.url, {'insert_into': 'top', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inserting_from_left(self):
        """
        original ids in row: [50, 26, 33, 11, 7, 16, 20]
        spare square: 36
        """
        expected_ids_in_row = [36, 50, 26, 33, 11, 7, 16]
        expected_spare_id = 20
        self.client.post(self.url, {'insert_into': 'left', 'insert_at': 2}, format='json')
        pieces = models.GamePiece.objects.filter(Q(order__range=(8, 14)), Q(game_id=self.game.id)).order_by('order').values_list('id', flat=True)
        pieces = list(pieces)
        spare_square = models.GamePiece.objects.get(game_id=self.game.id, order__isnull=True)
        self.assertEqual(expected_ids_in_row, pieces)
        self.assertEqual(spare_square.id, expected_spare_id)

    def test_inserting_from_right(self):
        """
        original ids in row: [50, 26, 33, 11, 7, 16, 20]
        spare square: 36
        """
        expected_ids_in_row = [26, 33, 11, 7, 16, 20, 36]
        expected_spare_id = 50
        self.client.post(self.url, {'insert_into': 'right', 'insert_at': 2}, format='json')
        pieces = models.GamePiece.objects.filter(Q(order__range=(8, 14)), Q(game_id=self.game.id)).order_by('order').values_list('id', flat=True)
        pieces = list(pieces)
        spare_square = models.GamePiece.objects.get(game_id=self.game.id, order__isnull=True)
        self.assertEqual(expected_ids_in_row, pieces)
        self.assertEqual(spare_square.id, expected_spare_id)

    def test_inserting_from_top(self):
        """
        original ids in column: [4, 11, 21, 31, 28, 18, 27]
        spare square: 36
        """
        expected_ids_in_column = [36, 4, 11, 21, 31, 28, 18]
        expected_spare_id = 27
        self.client.post(self.url, {'insert_into': 'top', 'insert_at': 4}, format='json')
        pieces = models.GamePiece.objects.annotate(
            ordermod=F('order') % 7
        ).filter(
            Q(ordermod=4),
            Q(game_id=self.game.id)
        ).order_by('order').values_list('id', flat=True)
        pieces = list(pieces)
        spare_square = models.GamePiece.objects.get(game_id=self.game.id, order__isnull=True)
        self.assertEqual(expected_ids_in_column, pieces)
        self.assertEqual(spare_square.id, expected_spare_id)

    def test_inserting_from_bottom(self):
        """
        original ids in column: [4, 11, 21, 31, 28, 18, 27]
        spare square: 36
        """
        expected_ids_in_column = [11, 21, 31, 28, 18, 27, 36]
        expected_spare_id = 4
        self.client.post(self.url, {'insert_into': 'bottom', 'insert_at': 4}, format='json')
        pieces = models.GamePiece.objects.annotate(
            ordermod=F('order') % 7
        ).filter(
            Q(ordermod=4),
            Q(game_id=self.game.id)
        ).order_by('order').values_list('id', flat=True)
        pieces = list(pieces)
        spare_square = models.GamePiece.objects.get(game_id=self.game.id, order__isnull=True)
        self.assertEqual(expected_ids_in_column, pieces)
        self.assertEqual(spare_square.id, expected_spare_id)

    def test_undoing_previous_player_insert_square(self):
        response = self.client.post(self.url, {'insert_into': 'bottom', 'insert_at': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

class CreateGameTest(APITestCase):
    fixtures = ['game/fixtures/data.json',]

    def setUp(self):
        self.first_user = User.objects.create_user('test_user1', 'test1@example.com', 'testpassword')
        self.second_user = User.objects.create_user('test_user2', 'test2@example.com', 'testpassword')
        token = Token.objects.get(user=self.first_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_game(self):
        """
        Ensure we can create a new game with a logged in user
        """
        url = reverse('game-list')
        response = self.client.post(url, {}, format='json')
        game = models.Game.objects.latest('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Game.objects.count(), 1)
        self.assertEqual(game.creator, self.first_user)
        self.assertEqual(game.winner, None)
        self.assertEqual(game.current_player, None)
        self.assertEqual(game.status, models.Game.LOBBY)

    def test_create_game_creates_player_counter(self):
        url = reverse('game-list')
        response = self.client.post(url, {}, format='json')
        game = models.Game.objects.latest('id')
        player = models.Player.objects.latest('id')
        self.assertEqual(models.Player.objects.count(), 1)
        self.assertEqual(player.user, self.first_user)
        self.assertEqual(player.game, game)
        self.assertEqual(player.game_piece, None)
        self.assertEqual(player.starting_game_piece, None)
        self.assertEqual(player.completed_time, None)
        self.assertEqual(player.starting_position, None)
        self.assertEqual(player.remaining_collectable_item_count(), 0)
        self.assertEqual(player.on_starting_square(), True)

    def test_create_game_creates_game_pieces(self):
        url = reverse('game-list')
        response = self.client.post(url, {}, format='json')
        game = models.Game.objects.latest('id')
        pieces = models.GamePiece.objects.filter(game=game)
        all_pieces = Count('pieces')
        board_pieces = Count('pieces', filter=Q(pieces__order__isnull=False))
        image_pieces = Count('pieces', filter=Q(pieces__collectable_item__isnull=False))
        straight_pieces = Count('pieces', filter=Q(pieces__orientation__shape__title='straight') & Q(pieces__collectable_item__isnull=True))
        tjunction_pieces = Count('pieces', filter=Q(pieces__orientation__shape__title='tjunction') & Q(pieces__collectable_item__isnull=False))
        bend_pieces_with_image = Count('pieces', filter=Q(pieces__orientation__shape__title='bend') & Q(pieces__collectable_item__isnull=False))
        bend_pieces_without_image = Count('pieces', filter=Q(pieces__orientation__shape__title='bend') & Q(pieces__collectable_item__isnull=True))
        game_pieces = models.Game.objects.filter(id=game.id).annotate(
            all=all_pieces,
            on_board=board_pieces,
            image_pieces=image_pieces,
            straight_pieces=straight_pieces,
            tjunction_pieces=tjunction_pieces,
            bend_pieces_with_image=bend_pieces_with_image,
            bend_pieces_without_image=bend_pieces_without_image
        )
        self.assertEqual(game_pieces[0].all, 50)
        self.assertEqual(game_pieces[0].on_board, 49)
        self.assertEqual(game_pieces[0].image_pieces, 24)
        self.assertEqual(game_pieces[0].straight_pieces, 12)
        self.assertEqual(game_pieces[0].tjunction_pieces, 18)
        self.assertEqual(game_pieces[0].bend_pieces_with_image, 6)
        self.assertEqual(game_pieces[0].bend_pieces_without_image, 14)

    def test_create_game_ensure_game_pieces_are_placed_correctly(self):
        url = reverse('game-list')
        response = self.client.post(url, {}, format='json')
        game = models.Game.objects.latest('id')
        order_list = [1,3,5,7,15,17,19,21,29,31,33,35,43,45,47,49]
        preserved = Case(*[When(order=order, then=pos) for pos, order in enumerate(order_list)])
        pieces = models.GamePiece.objects.filter(game_id=game.id, order__in=order_list).order_by(preserved).prefetch_related('orientation__shape')
        expected = (
            (1,1,False),(2,5,True),(2,5,True),(1,2,False),
            (2,7,True),(2,7,True),(2,5,True),(2,8,True),
            (2,7,True),(2,6,True),(2,8,True),(2,8,True),
            (1,3,False),(2,6,True),(2,6,True),(1,4,False),
        )
        current = 0
        for piece in pieces:
            shape, orientation, hasImage = expected[current]
            self.assertEqual(piece.orientation.shape.id, shape)
            self.assertEqual(piece.orientation.id, orientation)
            if hasImage:
                self.assertFalse(piece.collectable_item  == None)
            else:
                self.assertTrue(piece.collectable_item  == None)

            current = current + 1

        self.assertEqual(pieces.count(), 16)


    def test_create_game_not_logged_in(self):
        """
        Ensure we cannot create a new game with a logged out user
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('game-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(models.Game.objects.count(), 0)

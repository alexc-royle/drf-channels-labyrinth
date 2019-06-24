from django.contrib.auth.models import User
from django.db.models import Case, When, Q, Count, F
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
import json

from . import models
from . import views

# Create your tests here.

class ShapeTest(APITestCase):
    fixtures = ['game/fixtures/data.json',]

    def test_shapes(self):
        expected = ['bend', 'tjunction', 'straight']
        shapes = models.GamePieceShape.objects.all().order_by('id')
        self.assertEqual(shapes.count(), 3)
        for shape in shapes:
            self.assertEqual(shape.title, expected.pop(0))


class OrientationTest(APITestCase):
    fixtures = ['game/fixtures/data.json',]

    def test_orientations(self):
        expected = [
            (1, False, True, False, True),
            (1, False, True, True, False),
            (1, True, False, False, True),
            (1, True, False, True, False),
            (2, False, True, True, True),
            (2, True, False, True, True),
            (2, True, True, False, True),
            (2, True, True, True, False),
            (3, True, True, False, False),
            (3, False, False, True, True)
        ]
        orientations = models.GamePieceOrientation.objects.all().order_by('id')
        self.assertEqual(orientations.count(), 10)
        for orientation in orientations:
            shape, up, down, left, right = expected.pop(0)
            self.assertEqual(orientation.shape.id, shape)
            self.assertEqual(orientation.up, up)
            self.assertEqual(orientation.down, down)
            self.assertEqual(orientation.left, left)
            self.assertEqual(orientation.right, right)


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
        self.assertEqual(player.remaining_item_count(), 0)
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

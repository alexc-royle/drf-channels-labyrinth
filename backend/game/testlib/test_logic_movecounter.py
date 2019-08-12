from django.utils import timezone
from django.test import override_settings
from rest_framework.exceptions import ValidationError, ParseError
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
        self.game_piece = mommy.make('game.GamePiece', game=self.game, order=1)
        self.player = mommy.make('game.Player', game=self.game, order=1, game_piece=self.game_piece)

        self.game.current_player = self.player
        self.request = Mock()
        self.request.data = { 'movex': 0, 'movey': 1 }

    def test_init(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        self.assertEqual(moveCounter.game_pk, self.game.id)
        self.assertEqual(moveCounter.player, self.player)
        self.assertEqual(moveCounter.request, self.request)

    def test_process(self):
        given = {
            'parse_input': [0, 1],
            'get_changed': 'movey',
            'get_new_position_data': (8, 'down', 'up')
        }
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.parse_input = Mock(side_effect=given['parse_input'])
        moveCounter.get_changed = Mock(return_value=given['get_changed'])
        moveCounter.get_new_position_data = Mock(return_value=given['get_new_position_data'])
        moveCounter.update_position = Mock()
        moveCounter.process()
        moveCounter.parse_input.assert_called()
        self.assertEqual(moveCounter.parse_input.call_count, 2)
        moveCounter.get_changed.assert_called()
        moveCounter.get_new_position_data.assert_called()
        moveCounter.update_position.assert_called()
        self.assertEqual(moveCounter.movex, given['parse_input'][0])
        self.assertEqual(moveCounter.movey, given['parse_input'][1])
        self.assertEqual(moveCounter.value_changed, given['get_changed'])
        self.assertEqual(moveCounter.old_position, self.game_piece.order)
        self.assertEqual(moveCounter.new_position_data, given['get_new_position_data'])

    def test_parse_input_pass(self):
        given = 1
        expected = 1
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        received = moveCounter.parse_input(given)
        self.assertEqual(received, expected)

    def test_parse_input_pass_with_string(self):
        given = "1"
        expected = 1
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        received = moveCounter.parse_input(given)
        self.assertEqual(received, expected)

    def test_parse_input_fail_out_of_bounds(self):
        given = 2
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        with self.assertRaises(ValidationError):
            moveCounter.parse_input(given)

    def test_parse_input_fail_not_a_number(self):
        given = "a"
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        with self.assertRaises(ValidationError):
            moveCounter.parse_input(given)

    def test_get_changed_movex(self):
        given = { 'movex': 1, 'movey': 0 }
        expected = 'movex'
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        received = moveCounter.get_changed(given['movex'], given['movey'])
        self.assertEqual(received, expected)

    def test_get_changed_movey(self):
        given = { 'movex': 0, 'movey': 1 }
        expected = 'movey'
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        received = moveCounter.get_changed(given['movex'], given['movey'])
        self.assertEqual(received, expected)

    def test_get_changed_fail_neither_moved(self):
        given = { 'movex': 0, 'movey': 0 }
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        with self.assertRaises(ValidationError):
            moveCounter.get_changed(given['movex'], given['movey'])

    def test_get_changed_fail_both_moved(self):
        given = { 'movex': 1, 'movey': 1 }
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        with self.assertRaises(ValidationError):
            moveCounter.get_changed(given['movex'], given['movey'])

    def test_get_new_position_data_x(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.get_new_position_x = Mock()
        moveCounter.get_new_position_y = Mock()
        moveCounter.value_changed = 'movex'
        moveCounter.get_new_position_data()
        moveCounter.get_new_position_x.assert_called()
        moveCounter.get_new_position_y.assert_not_called()

    def test_get_new_position_data_y(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.get_new_position_x = Mock()
        moveCounter.get_new_position_y = Mock()
        moveCounter.value_changed = 'movey'
        moveCounter.get_new_position_data()
        moveCounter.get_new_position_x.assert_not_called()
        moveCounter.get_new_position_y.assert_called()

    def test_get_new_position_x_high(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.within_bounds_x = Mock()
        moveCounter.old_position = 5
        moveCounter.movex = 1
        expected = (6, 'right', 'left')
        received = moveCounter.get_new_position_x()
        self.assertEqual(expected, received)
        moveCounter.within_bounds_x.assert_called()

    def test_get_new_position_x_low(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.within_bounds_x = Mock()
        moveCounter.old_position = 5
        moveCounter.movex = -1
        expected = (4, 'left', 'right')
        received = moveCounter.get_new_position_x()
        self.assertEqual(expected, received)
        moveCounter.within_bounds_x.assert_called()

    def test_within_bounds_x_too_low_error(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.old_position = 1
        moveCounter.movex = -1
        with self.assertRaises(ValidationError):
            moveCounter.within_bounds_x()

    def test_within_bounds_x_too_high_error(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.old_position = 7
        moveCounter.movex = 1
        with self.assertRaises(ValidationError):
            moveCounter.within_bounds_x()

    def test_within_bounds_x(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.old_position = 5
        moveCounter.movex = 1
        try:
            moveCounter.within_bounds_x()
            self.assertEqual(True, True)
        except ValidationError:
            self.assertEqual(False, True)

    def test_get_new_position_y_high(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.within_bounds_y = Mock()
        moveCounter.old_position = 10
        moveCounter.movey = 1
        expected = (17, 'down', 'up')
        received = moveCounter.get_new_position_y()
        self.assertEqual(expected, received)
        moveCounter.within_bounds_y.assert_called()

    def test_get_new_position_y_low(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.within_bounds_y = Mock()
        moveCounter.old_position = 10
        moveCounter.movey = -1
        expected = (3, 'up', 'down')
        received = moveCounter.get_new_position_y()
        self.assertEqual(expected, received)
        moveCounter.within_bounds_y.assert_called()

    def test_within_bounds_y_too_low_error(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.old_position = 5
        moveCounter.movey = -1
        with self.assertRaises(ValidationError):
            moveCounter.within_bounds_y()

    def test_within_bounds_y_too_high_error(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.old_position = 44
        moveCounter.movey = 1
        with self.assertRaises(ValidationError):
            moveCounter.within_bounds_y()

    def test_within_bounds_y(self):
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.old_position = 20
        moveCounter.movey = 1
        try:
            moveCounter.within_bounds_y()
            self.assertEqual(True, True)
        except ValidationError:
            self.assertEqual(False, True)

    def test_update_position_ok(self):
        old_orientation = mommy.make('game.GamePieceOrientation', right=True)
        new_orientation = mommy.make('game.GamePieceOrientation', left=True)
        self.game_piece.orientation = old_orientation
        new_game_piece = mommy.make('game.GamePiece', game=self.game, order=2, orientation=new_orientation)
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.new_position_data = (2, 'right', 'left')
        moveCounter.update_position()
        self.assertEqual(self.player.game_piece, new_game_piece)

    def test_update_position_error(self):
        old_orientation = mommy.make('game.GamePieceOrientation', right=True)
        new_orientation = mommy.make('game.GamePieceOrientation', left=False)
        self.game_piece.orientation = old_orientation
        new_game_piece = mommy.make('game.GamePiece', game=self.game, order=2, orientation=new_orientation)
        moveCounter = logic.MoveCounter(self.request, self.game.id, self.player)
        moveCounter.new_position_data = (2, 'right', 'left')
        with self.assertRaises(ValidationError):
            moveCounter.update_position()

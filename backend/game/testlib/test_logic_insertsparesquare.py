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

@override_settings(SUSPEND_SIGNALS=True)
class InsertSpareSquareTest(APITestCase):
    def setUp(self):
        self.game = mommy.make('game.Game', status=models.Game.INPROGRESS)
        self.gamepieces = [mommy.make('game.GamePiece', id=n, order=n, game=self.game) for n in range(1, 50)]
        self.spare_square = mommy.make('game.GamePiece', id=50, order=None, game=self.game)
        self.player = mommy.make('game.Player', game=self.game, order=1, game_piece=self.gamepieces[0])
        self.playerturn = mommy.make('game.PlayerTurn', player=self.player)
        self.insert_into = 'left'
        self.insert_at = 2

    def test_init(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, self.insert_at)
        self.assertEqual(insertSpareSquare.game, self.game)
        self.assertEqual(insertSpareSquare.player, self.player)
        self.assertEqual(insertSpareSquare.insert_into, self.insert_into)
        self.assertEqual(insertSpareSquare.insert_at, self.insert_at)
        self.assertEqual(insertSpareSquare.turn, self.playerturn)

    def test_process(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, self.insert_at)
        insertSpareSquare.check_turn = Mock()
        insertSpareSquare.validate = Mock()
        insertSpareSquare.convert_insert_at = Mock()
        insertSpareSquare.check_previous_turn = Mock()
        insertSpareSquare.insert_spare_square = Mock()
        insertSpareSquare.process()
        insertSpareSquare.check_turn.assert_called()
        insertSpareSquare.validate.assert_called()
        insertSpareSquare.convert_insert_at.assert_called()
        insertSpareSquare.check_previous_turn.assert_called()
        insertSpareSquare.insert_spare_square.assert_called()

    def test_checkturn_error(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, self.insert_at)
        insertSpareSquare.turn.turn_status = models.PlayerTurn.POST_INSERT_SPARESQUARE
        with self.assertRaises(ValidationError):
            insertSpareSquare.check_turn()

    def test_validate_missing(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, None, self.insert_at)
        with self.assertRaises(ValidationError):
            insertSpareSquare.validate()

    def test_validate_unknown_into(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, 'hello', self.insert_at)
        with self.assertRaises(ValidationError):
            insertSpareSquare.validate()

    def test_validate_unknown_at(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, 3)
        with self.assertRaises(ValidationError):
            insertSpareSquare.validate()

    def test_convert_insert_at(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, 'hello')
        with self.assertRaises(ValidationError):
            insertSpareSquare.convert_insert_at()

    def test_check_previous_turn(self):
        previousTurn = mommy.make('game.PlayerTurn', player=self.player, turn_status=models.PlayerTurn.POST_INSERT_SPARESQUARE, spare_square_inserted_into='right', spare_square_inserted_at=2)
        newTurn = mommy.make('game.PlayerTurn', player=self.player)
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, self.insert_at)

        with self.assertRaises(ValidationError):
            insertSpareSquare.check_previous_turn()

    def test_insert_spare_square(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, self.insert_at)
        insertSpareSquare.get_pieces = Mock()
        insertSpareSquare.get_order = Mock()
        insertSpareSquare.get_order_numbers = Mock()
        insertSpareSquare.update_orders = Mock()
        insertSpareSquare.update_turn = Mock()

        insertSpareSquare.insert_spare_square()

        insertSpareSquare.get_pieces.assert_called()
        insertSpareSquare.get_order.assert_called()
        insertSpareSquare.get_order_numbers.assert_called()
        insertSpareSquare.update_orders.assert_called()
        insertSpareSquare.update_turn.assert_called()

    def test_get_pieces_top_bottom(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, 'top', self.insert_at)
        insertSpareSquare.get_pieces_by_column = Mock(return_value='column')
        insertSpareSquare.get_pieces_by_row = Mock(return_value='row')

        received = insertSpareSquare.get_pieces()
        self.assertEqual(received, 'column')
        insertSpareSquare.get_pieces_by_column.assert_called()
        insertSpareSquare.get_pieces_by_row.assert_not_called()

    def test_get_pieces_left_right(self):
        insertSpareSquare = logic.InsertSpareSquare(self.game, self.player, self.insert_into, self.insert_at)
        insertSpareSquare.get_pieces_by_column = Mock(return_value='column')
        insertSpareSquare.get_pieces_by_row = Mock(return_value='row')

        received = insertSpareSquare.get_pieces()
        self.assertEqual(received, 'row')
        insertSpareSquare.get_pieces_by_column.assert_not_called()
        insertSpareSquare.get_pieces_by_row.assert_called()

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
class FinishTurnTest(APITestCase):
    def setUp(self):
        self.game = mommy.make('game.Game', status=models.Game.INPROGRESS)
        self.players = [
            mommy.make('game.Player', game=self.game, order=1),
            mommy.make('game.Player', game=self.game, order=2, completed_time=timezone.now()),
            mommy.make('game.Player', game=self.game, order=3),
            mommy.make('game.Player', game=self.game, order=4)
        ]
        self.game.current_player = self.players[0]


    def test_process_game_in_progress(self):
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        finishTurn.check_if_completed = Mock(return_value = False)
        finishTurn.set_current_player = Mock()
        finishTurn.check_player_on_collectable = Mock()
        finishTurn.process()
        finishTurn.check_if_completed.assert_called()
        finishTurn.check_player_on_collectable.assert_called()
        finishTurn.set_current_player.assert_called()

    def test_process_game_completed(self):
        self.game.status = models.Game.COMPLETED
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        finishTurn.check_if_completed = Mock()
        finishTurn.set_current_player = Mock()
        finishTurn.check_player_on_collectable = Mock()
        finishTurn.process()
        finishTurn.check_if_completed.assert_called()
        finishTurn.set_current_player.assert_not_called()
        finishTurn.check_player_on_collectable.assert_not_called()

    def test_should_continue_not_all_others_completed(self):
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        returned = finishTurn.should_continue()
        self.assertEqual(returned, True)

    def test_should_continue_all_others_completed(self):
        self.players[2].completed_time=timezone.now()
        self.players[2].save()
        self.players[3].completed_time=timezone.now()
        self.players[3].save()
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        returned = finishTurn.should_continue()
        self.assertEqual(returned, False)

    def test_should_continue_one_player_completed(self):
        game = mommy.make('game.Game', status=models.Game.INPROGRESS)
        player = mommy.make('game.Player', game=self.game, order=1, completed_time=timezone.now())
        finishTurn = logic.FinishTurn(game, player)
        returned = finishTurn.should_continue()
        self.assertEqual(returned, False)

    def test_set_current_player_to_next(self):
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        self.game.save = Mock()
        finishTurn.set_current_player()
        self.assertEqual(self.game.current_player.id, self.players[2].id)
        self.game.save.assert_called()

    def test_set_current_player_to_first(self):
        self.game.current_player = self.players[3]
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        self.game.save = Mock()
        finishTurn.set_current_player()
        self.assertEqual(self.game.current_player.id, self.players[0].id)
        self.game.save.assert_called()

    def test_check_if_completed(self):
        self.game.current_player.remaining_collectable_item_count = Mock(return_value = 0)
        self.game.current_player.on_starting_square = Mock(return_value = True)
        self.game.current_player.save = Mock()
        self.game.save = Mock()
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        finishTurn.should_continue = Mock(return_value = False)
        returned = finishTurn.check_if_completed()
        self.game.current_player.remaining_collectable_item_count.assert_called()
        self.game.current_player.on_starting_square.assert_called()
        self.game.current_player.save.assert_called()
        self.game.save.assert_called()
        finishTurn.should_continue.assert_called()
        self.assertEqual(returned, True)

    def test_check_if_completed_remaining_items(self):
        self.game.current_player.remaining_collectable_item_count = Mock(return_value = 5)
        self.game.current_player.on_starting_square = Mock()
        self.game.current_player.save = Mock()
        self.game.save = Mock()
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        finishTurn.should_continue = Mock()
        returned = finishTurn.check_if_completed()
        self.game.current_player.remaining_collectable_item_count.assert_called()
        self.game.current_player.on_starting_square.assert_not_called()
        self.game.current_player.save.assert_not_called()
        self.game.save.assert_not_called()
        finishTurn.should_continue.assert_not_called()
        self.assertEqual(returned, False)

    def test_check_if_completed_not_on_starting_square(self):
        self.game.current_player.remaining_collectable_item_count = Mock(return_value = 0)
        self.game.current_player.on_starting_square = Mock(return_value = False)
        self.game.current_player.save = Mock()
        self.game.save = Mock()
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        finishTurn.should_continue = Mock()
        returned = finishTurn.check_if_completed()
        self.game.current_player.remaining_collectable_item_count.assert_called()
        self.game.current_player.on_starting_square.assert_called()
        self.game.current_player.save.assert_not_called()
        self.game.save.assert_not_called()
        finishTurn.should_continue.assert_not_called()
        self.assertEqual(returned, False)

    def test_check_player_on_collectable(self):
        collectable_item = mommy.make('game.CollectableItem')
        player_collectable_item = mommy.make('game.PlayerCollectableItem', collectable_item = collectable_item, collected = False)
        self.game.current_player.on_next_collectable_item = Mock(return_value = True)
        self.game.current_player.next_collectable_item = Mock(return_value = collectable_item)
        player_collectable_item.save = Mock()
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        finishTurn.check_player_on_collectable()
        self.game.current_player.on_next_collectable_item.assert_called()
        self.game.current_player.next_collectable_item.assert_called()
        player_collectable_item.save.assert_called()
        self.assertEqual(player_collectable_item.collected, True)

    def test_check_player_on_collectable_not(self):
        collectable_item = mommy.make('game.CollectableItem')
        player_collectable_item = mommy.make('game.PlayerCollectableItem', collectable_item = collectable_item, collected = False)
        self.game.current_player.on_next_collectable_item = Mock(return_value = False)
        self.game.current_player.next_collectable_item = Mock()
        player_collectable_item.save = Mock()
        finishTurn = logic.FinishTurn(self.game, self.game.current_player)
        finishTurn.check_player_on_collectable()
        self.game.current_player.on_next_collectable_item.assert_called()
        self.game.current_player.next_collectable_item.assert_not_called()
        player_collectable_item.save.assert_not_called()

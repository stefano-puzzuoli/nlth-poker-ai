#!/usr/bin/env python3

import unittest
from sklearn.ensemble import GradientBoostingRegressor
import sys
sys.path.append("..")                                   	# allows imports from parent directories
from ai_poker.templates import BasicPlayer, simulate
from ai_poker.gamestate import GameState

class TestBasicPlayer(unittest.TestCase):
	''' Class for running unittests on functionalities of BasicPlayer in templates.py '''

	def setUp(self):
		''' SetUp BasicPlayer object '''
		regressor = GradientBoostingRegressor()
		basicPlayer = BasicPlayer(name="BasicPlayer", reg=regressor, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
		self.players = [basicPlayer]
		self.player = basicPlayer
		self.gamestate = GameState(self.players)

	def test_gen_action_features(self):
		''' SetUp BasicPlayer object '''
		foldAction = ["fold"]
		self.assertTrue(self.player.gen_action_features(foldAction, self.gamestate))

		checkAction = ["check"]
		self.assertTrue(self.player.gen_action_features(checkAction, self.gamestate))

		callAction = ["call"]
		self.assertTrue(self.player.gen_action_features(callAction, self.gamestate))


	def test_buy_chips(self):
		''' Test the player buy chips in game action'''
		self.player.buy_chips(25000)
		self.assertEqual(self.player.stack, 25000)

	def test_cash_out(self):
		''' Test the player cash out in game action'''
		self.player.cash_out()
		self.assertEqual(self.player.stack, 0)

	def test_remove_chips(self):
		''' Test the player remove chips in game action'''
		self.player.buy_chips(25000)
		oldStack = self.player.stack
		self.player.remove_chips(20000)
		self.assertEqual(self.player.stack, 5000)

	def test_add_chips(self):
		''' Test the player add chips in game action'''
		self.player.buy_chips(25000)
		oldStack = self.player.stack
		self.player.add_chips(5000)
		self.assertEqual(self.player.stack, 30000)

	def test_start_training(self):
		''' Test that player start training as expected'''
		self.player.start_training()
		self.assertTrue(self.player.train)

	def test_stop_training(self):
		''' Test that player stop training as expected'''
		self.player.stop_training()
		self.assertFalse(self.player.train)


def main():
	test = TestBasicPlayer()
	test.setUp()
	test.test_gen_action_features()
	test.test_buy_chips()
	test.test_cash_out()
	test.test_remove_chips()
	test.test_add_chips()
	test.test_start_training()
	test.test_stop_training()


if __name__ == "__main__":
	main()
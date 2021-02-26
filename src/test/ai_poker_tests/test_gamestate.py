#!/usr/bin/env python3

import unittest
from sklearn.ensemble import GradientBoostingRegressor
import sys
sys.path.append("..")                                   # allows imports from parent directories
from ai_poker.gamestate import GameState
from ai_poker.templates import BasicPlayer


class TestGameState(unittest.TestCase):
	''' Class for running unittests on functionalities of gamestate.py '''

	def setUp(self):
		''' SetUp GameState object '''

		# add players to table
		players = []
		for i in range(5):
			regressor = GradientBoostingRegressor()
			name = 'Player ' + str(i+1)
			p = BasicPlayer(name=name, reg=regressor, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
			players.append(p)

		regressor = GradientBoostingRegressor()
		name = 'Player ' + str(i+1)
		p = BasicPlayer(name="User", reg=regressor, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
		players.append(p)

		self.players = players
		self.gamestate = GameState(players)

	def test_gamestate_set_up(self):
		''' Test that a GameState object is reset as expected (behaviour expected before each hand)'''

		self.assertEqual(self.gamestate.to_call, None)
		self.assertEqual(self.gamestate.min_raise, None) 
		self.assertEqual(self.gamestate.num_players, len(self.players)) 
		self.assertFalse(self.gamestate.folded) 
		self.assertFalse(self.gamestate.all_in) 
		self.assertFalse(self.gamestate.cards) 
		self.assertFalse(self.gamestate.actor) 


def main():
	test = TestGameState()
	test.setUp()
	test.test_gamestate_set_up()

if __name__ == "__main__":
	main()

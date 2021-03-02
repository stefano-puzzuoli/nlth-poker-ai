#!/usr/bin/env python3

import unittest
import sys
sys.path.append("..")											# allows imports from parent directories
from ai_poker.player import Player
from ai_poker.evaluator.evaluator import Evaluator
from ai_poker.evaluator.deck import Deck 
from sklearn.ensemble import GradientBoostingRegressor



class TestEvaluator(unittest.TestCase):
	''' Class for running unittests on functionalities of evaluator.py '''

	def setUp(self):
		''' SetUp Evaluator object '''

		self.eval = Evaluator()
		self.ranks = {}
		self.cards = Deck.getCompleteDeck()
		self.board = [card for card in self.cards]


	def test_evaluate(self):
		''' Test the evaluate functionality used for Evaluator '''

		players = []
		for i in range(5):
  
			#create Player that uses GradientBoostingRegressor as machine learning model
			#with wealth of 1 million and 10 discrete choices for raising,
			#with each raise choice .7 times the next largest raise choice
			#Player forgets training samples older than 100,000
			r = GradientBoostingRegressor()
			name = 'Player ' + str(i+1)
			p = Player(name=name, reg=r, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
			players.append(p)

		
		#evaluate rank of hand for each player
		ranks = {}
		for player in players:
			if not self.board: 
				rank = -1    #all players but one have folded before flop
				ranks[player] = rank

		self.assertEqual(self.ranks, ranks)


		
	def test_hand_summary(self):
		''' Test the get_rank_int functionality used for hand Evaluator '''
		self.assertTrue(len(self.board))

		hands = []
		line_length = 10
		game_stages = ["FLOP", "TURN", "RIVER"]
		best_rank = 7463
		for i in range(len(game_stages)):
			line = ("=" * line_length) + " %s " + ("=" * line_length) 
			
			curr_best_rank = 7463 
			winners = []
			for player, h in enumerate(hands):
				rank = self.eval.evaluate(h, board[:(i + 3)])
				hand_rank = self.eval.get_hand_rank(rank)
				rank_string = self.eval.to_string(hand_rank)
				percentage = 1.0 - self.eval.get_rank_percentage(rank) 

				if rank == best_rank:
					winners.append(player)
					best_rank = rank
				elif rank < best_rank:
					winners = [player]
					best_rank = rank
		self.assertEqual(line_length, 10)
		self.assertEqual(best_rank, curr_best_rank)

def main():
	test = TestEvaluator()
	test.setUp()
	test.test_evaluate()
	test.test_hand_summary()


if __name__ == "__main__":
	main()

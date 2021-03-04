#!/usr/bin/env python3

from random import shuffle
import unittest
import sys
sys.path.append("..")											# allows imports from parent directories
from ai_poker.evaluator.evaluator import Evaluator
from ai_poker.evaluator.lookup import LookupTable
from ai_poker.evaluator.card_service import CardService



class TestLookUp(unittest.TestCase):
	''' Class for running unittests on functionalities of lookup.py '''

	def test_rank_strings(self):
		''' Test the rank_strings mappings used for Evaluator ''' 
		rank_strings = {
		1 : "Straight Flush",
		2 : "Four of a Kind",
		3 : "Full House",
		4 : "Flush",
		5 : "Straight",
		6 : "Three of a Kind",
		7 : "Two Pair",
		8 : "Pair",
		9 : "High Card"
		}

		for rank in rank_strings:
			self.assertEqual(rank_strings[rank], LookupTable.rank_string[rank])

	def test_hand_rank(self):
		''' Test the hand_rank mappings used for Evaluator ''' 

		s_flush  = 10
		four_kind = 166
		f_house = 322 
		flush = 1599
		straight = 1609
		three_kind = 2467
		two_pair = 3325
		pair = 6185
		h_card = 7462

		hand_rank = {
		s_flush: 1,
		four_kind: 2,
		f_house: 3,
		flush: 4,
		straight: 5,
		three_kind: 6,
		two_pair: 7,
		pair: 8,
		h_card: 9
		}

		hand_value = 1
		for rank in hand_rank:
			self.assertEqual(hand_rank[rank], hand_value)
			hand_value += 1


	def test_flushes_lookup(self):
		''' Test the flushes lookup used for Evaluator ''' 
		s_flushes = [
			7936,
			3968,
			1984,
			992,
			496,
			248, 
			124, 
			62, 
			31, 
			4111 
		]

		expectedFlushRank = 323

		flushes = []

		flushes.reverse()
		rank = 1
		for sf in s_flushes:
			prime_product = CardService.prime_product_from_rankings(sf)
			rank += 1

		rank = LookupTable.f_house + 1
		for f in flushes:
			prime_product = CardService.prime_product_from_rankings(f)
			rank += 1

		self.assertEqual(rank, expectedFlushRank)
		

def main():
	test = TestLookUp()
	test.setUp()
	test.test_rank_strings()
	test.test_hand_rank()
	test.test_flushes_lookup()


if __name__ == "__main__":
	main()

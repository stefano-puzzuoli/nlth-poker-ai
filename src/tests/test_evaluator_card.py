#!/usr/bin/env python3

import unittest
import sys
sys.path.append("..")											# allows imports from parent directories
from ai_poker.evaluator.card_service import CardService


class TestCardService(unittest.TestCase):
	''' Class for running unittests on functionalities of evaluator_card.py '''

	def test_get_rank_int(self):
		''' Test the get_rank_int functionality used for hand Evaluator '''
		self.assertEqual(CardService.get_rank_int(2), 2 >> 8 & 0xF)

		# check for 10, J, Q, K and A
		self.assertEqual(CardService.get_rank_int(10), 10 >> 8 & 0xF)
		self.assertEqual(CardService.get_rank_int(11), 11 >> 8 & 0xF)
		self.assertEqual(CardService.get_rank_int(12), 12 >> 8 & 0xF)
		self.assertEqual(CardService.get_rank_int(13), 13 >> 8 & 0xF)
		self.assertEqual(CardService.get_rank_int(14), 14 >> 8 & 0xF)
		self.assertEqual(CardService.get_rank_int(15), 15 >> 8 & 0xF)

	def test_get_suit_int(self):
		''' Test the get_suit_int functionality used for hand Evaluator '''
		self.assertEqual(CardService.get_suit_int(2), 2 >> 8 & 0xF)

		# check for 10, J, Q, K and A
		self.assertEqual(CardService.get_suit_int(10), 10 >> 12 & 0xF)
		self.assertEqual(CardService.get_suit_int(11), 11 >> 12 & 0xF)
		self.assertEqual(CardService.get_suit_int(12), 12 >> 12 & 0xF)
		self.assertEqual(CardService.get_suit_int(13), 13 >> 12 & 0xF)
		self.assertEqual(CardService.get_suit_int(14), 14 >> 12 & 0xF)
		self.assertEqual(CardService.get_suit_int(15), 15 >> 12 & 0xF)



def main():
	test = TestCardService()
	test.test_get_rank_int()
	test.test_get_suit_int()
	test.test_prime_product_from_hand()


if __name__ == "__main__":
	main()

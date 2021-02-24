import unittest
import sys
sys.path.append("..")                             # allows imports from parent directories
from ai_poker.table import Table


class TestAIModel(unittest.TestCase):
    ''' Class for running unittests on functionalities of game.py '''

    def setUp(self):
        ''' SetUp Table object '''
        try:
            table = Table(small_bind=10, big_blind=20, max_buy_in=20000)
            self.assertNotEqual(table, None)
        except IOError:
            print("Error: Cannot create Poker Table")

    def test_dataFrame_constructed_as_expected(self):
        ''' Test that the dataframe read in as expected'''
        return


    ## TEST EACH INDIVIDUAL COMPONENT

    


def main():
    test = TestAIModel()
    test.setUp()

if __name__ == "__main__":
    main()

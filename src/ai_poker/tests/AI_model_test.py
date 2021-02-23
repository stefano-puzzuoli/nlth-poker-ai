import unittest
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from pandas.testing import assert_frame_equal     # for testing dataframes
from pandas.testing import assert_series_equal    # for testing series
import sys
sys.path.append("..")
from table import Table


class AI_model_test(unittest.TestCase):
    ''' Class for running unittests on functionalities of play_game.py '''

    def setUp(self):
        ''' SetUp dataframe '''
        try:
            table = Table(small_bind=10, big_blind=20, max_buy_in=20000)
        except IOError:
            print("Cannot create Poker Table")

    


def main():
    df = Prediction_model_test()
    df.setUp()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import unittest
from sklearn.ensemble import GradientBoostingRegressor
import sys
sys.path.append("..")                                   # allows imports from parent directories
from ai_poker.table import Table
from ai_poker.simulation import simulate
from ai_poker.player import Player



class TestAIModel(unittest.TestCase):
    ''' Class for running unittests on functionalities of game.py '''

    def setUp(self):
        ''' SetUp Table object '''
        try:
            table = Table(small_bind=10, big_blind=20, max_buy_in=20000)
            self.table = table
        except IOError:
            print("Error: Cannot create Poker Table")

        # add players to table
        players = []
        for i in range(5):
            regressor = GradientBoostingRegressor()
            name = 'Player ' + str(i+1)
            p = Player(name=name, reg=regressor, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
            players.append(p)

        regressor = GradientBoostingRegressor()
        name = 'Player ' + str(i+1)
        p = Player(name="User", reg=regressor, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
        players.append(p)

        for p in players: self.table.add_player(p)

    def test_table_creation(self):
        ''' Test that the table object is created as expected'''

        # create table for comparison
        otherTable = Table(small_bind=10, big_blind=20, max_buy_in=20000)

        # check small blind assigned correctly
        self.assertEqual(self.table.small_bind, otherTable.small_bind)

        # check big blind assigned correctly
        self.assertEqual(self.table.big_blind, otherTable.big_blind)

        # check max buy in assigned correctly
        self.assertEqual(self.table.max_buy_in, otherTable.max_buy_in)


    def test_players_added(self):
        ''' Test that the players are added to the table as expected'''

        # create table for comparison
        otherTable = Table(small_bind=10, big_blind=20, max_buy_in=20000)
        # add players to comparison table
        players = []
        for i in range(5):
            r = GradientBoostingRegressor()
            name = 'Player ' + str(i+1)
            p = Player(name=name, reg=r, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
            players.append(p)

        r = GradientBoostingRegressor()
        name = 'Player ' + str(i+1)
        p = Player(name="User", reg=r, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
        players.append(p)

        for p in players: otherTable.add_player(p)

        # check that both lists have same numebr of players
        self.assertEqual(len(self.table.players), len(otherTable.players))

    def test_ai_game_simulation(self):
        ''' Test that AI game simulation executes as expected'''
        self.assertNotEqual(simulate(self.table, n_hands=5, first_train=5, n_train=5, n_buy_in=5), None)
    

def main():
    test = TestAIModel()
    test.setUp()
    test.test_table_creation()
    test.test_players_added()
    test.test_ai_game_simulation()

if __name__ == "__main__":
    main()

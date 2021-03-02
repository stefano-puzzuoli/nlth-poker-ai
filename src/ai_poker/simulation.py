#!/usr/bin/env python3

import time

from ai_poker.player import Player


def simulate(table, n_hands, first_train=0, n_train=0, n_buy_in=0, t_print=5, vocal=False):
    """
    This function simulates several hands of Holdem according to these parameters:

    Parameters:
    table - table used in simulation (Table)
    n_hands - total number of hands to simulate (int)
    first_train - number of hands before first training, when players take random actions (int)
    n_train - number of hands between training players (int)
    n_buy_in - number of hands between cashing out/buying in players (int)
    t_print - number of seconds between printing hand number (int)
    vocal - hands are narrated by table when vocal is True (bool)
    """

    print('Beginning simulation of', n_hands, 'hands.')

    players = table.get_players()
    # holds bankroll history of all players
    bankroll = [[] for player in players]
    max_buy_in = table.get_params()[-1]

    # set Player stack sizes to max buy-in or less
    for player in players:
        player.cash_out()
        if player.get_stack() < max_buy_in:
            player.buy_chips(max_buy_in)

    next_train = first_train  # next hand players will train
    if first_train == 0:
        next_train = n_train
    next_buy_in = n_buy_in  # next hand players will cash out and buy in
    hand = 1  # hands started
    last_time = time.time()  # last time printed hands completed
    while hand <= n_hands:

        if time.time() - last_time > t_print:
            last_time = time.time()
            print(hand - 1, 'hands simulated.')

        if hand == next_train:
            print('Players are training...')
            for player in players:
                player.train_player()
            next_train = hand + n_train
            print('Complete.')

        if hand == next_buy_in:
            if vocal:
                print('Players are cashing out and buying in.')
            for player in players:
                player.cash_out()
                if player.get_stack() < max_buy_in:
                    player.buy_chips(max_buy_in)
            next_buy_in = hand + n_buy_in

        if vocal:
            print('Hand', hand)
        played = table.play_hand(vocal=vocal)

        # Hand failure
        if not played:
            if next_buy_in == hand + n_buy_in:  # if players just bought in
                print('All or all but one players are bankrupt.')
                break

            # buy in and redo hand
            if vocal:
                print('Game over.')
                for player in players:
                    if (player.get_stack() != 0):
                        print(player.get_name() + " is the winner.")
                break
            next_buy_in = hand

        else:
            hand += 1
            for i in range(len(players)):
                bankroll[i].append(players[i].get_bankroll())

    print('Simulation complete.\n')
    return bankroll
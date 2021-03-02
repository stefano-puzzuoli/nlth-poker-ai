
import time

from ai_poker.player import Player


def simulate(table, num_hands, hands_before_training=0, hands_between_training=0, hands_between_buyin=0, t_print=5, narrate_hands=False):
    """
    This function simulates several hands of Holdem according to these parameters:

    Parameters:
    table - table used in simulation (Table)
    num_hands - total number of hands to simulate (int)
    hands_before_training - number of hands before first training, when players take random actions (int)
    hands_between_training - number of hands between training players (int)
    hands_between_buyin - number of hands between cashing out/buying in players (int)
    t_print - number of seconds between printing hand number (int)
    narrate_hands - hands are narrated by table when narrate_hands is True (bool)
    """

    print('Beginning simulation of', num_hands, 'hands.')

    players = table.get_players()
    # holds chips_amount history of all players
    chips_amount = [[] for player in players]
    max_buy_in = table.get_params()[-1]

    # set Player stack sizes to max buy-in or less
    for player in players:
        player.cash_out()
        if player.get_stack() < max_buy_in:
            player.buy_chips(max_buy_in)

    next_train = hands_before_training  # next hand players will train
    if hands_before_training == 0:
        next_train = hands_between_training
    next_buy_in = hands_between_buyin  # next hand players will cash out and buy in
    hand = 1  # hands started
    last_time = time.time()  # last time printed hands completed
    while hand <= num_hands:

        if time.time() - last_time > t_print:
            last_time = time.time()
            print(hand - 1, 'hands simulated.')

        if hand == next_train:
            print('Players are training...')
            for player in players:
                player.train_player()
            next_train = hand + hands_between_training
            print('Complete.')

        if hand == next_buy_in:
            if narrate_hands:
                print('Players are cashing out and buying in.')
            for player in players:
                player.cash_out()
                if player.get_stack() < max_buy_in:
                    player.buy_chips(max_buy_in)
            next_buy_in = hand + hands_between_buyin

        if narrate_hands:
            print('Hand', hand)
        played = table.play_hand(narrate_hands=narrate_hands)

        # Hand failure
        if not played:
            if next_buy_in == hand + hands_between_buyin:  # if players just bought in
                print('All or all but one players are bankrupt.')
                break

            # buy in and redo hand
            if narrate_hands:
                print('Game over.')
                for player in players:
                    if (player.get_stack() != 0):
                        print(player.get_name() + " is the winner.")
                break
            next_buy_in = hand

        else:
            hand += 1
            for i in range(len(players)):
                chips_amount[i].append(players[i].get_chips_amount())

    print('Simulation complete.\n')
    return chips_amount
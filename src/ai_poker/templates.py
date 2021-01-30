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
    bankroll = [[] for player in players]    #holds bankroll history of all players
    max_buy_in = table.get_params()[-1]

    #set Player stack sizes to max buy-in or less
    for player in players: 
        player.cash_out()
        if player.get_stack() < max_buy_in: player.buy_chips(max_buy_in)

    next_train = first_train    #next hand players will train
    if first_train == 0: next_train = n_train
    next_buy_in = n_buy_in        #next hand players will cash out and buy in
    hand = 1                  #hands started
    last_time = time.time()    #last time printed hands completed
    while hand <= n_hands:

        if time.time() - last_time > t_print:
            last_time = time.time()
            print(hand - 1, 'hands simulated.')
        
        if hand == next_train:
            print('Players are training...')
            for player in players: player.train_player()
            next_train = hand + n_train
            print('Complete.')

        if hand == next_buy_in:
            if vocal: print('Players are cashing out and buying in.')
            for player in players:
                player.cash_out()
                if player.get_stack() < max_buy_in: player.buy_chips(max_buy_in)
            next_buy_in = hand + n_buy_in

        if vocal: print('Hand', hand)
        played = table.play_hand(vocal=vocal)
        
        #Hand failure
        if not played:    
            if next_buy_in == hand + n_buy_in:    #if players just bought in
                print('All or all but one players are bankrupt.')
                break

            #buy in and redo hand
            if vocal: 
                print('Game over.')
                for player in players: 
                    if (player.get_stack() != 0):
                        print(player.get_name() + " is the winner.") 
                break
            next_buy_in = hand    
        
        else:
            hand += 1
            for i in range(len(players)): bankroll[i].append(players[i].get_bankroll())

    print('Simulation complete.\n')
    return bankroll

class BasicPlayer(Player):

    def gen_game_features(self, game_state):

        """ 
        This method generates a set of features from a game_state and independently of the
        action a player takes. 
        """

        game_features = 43 * [0]

        hold_cards = sorted(self.cards)
        table_cards = sorted(game_state.cards)

        #add number and suit of each card to features
        cards = hold_cards + table_cards
        for i in range(len(cards)):
            game_features[6 * i] = 1    #ith card exists
            game_features[6 * i + 1] = cards[i].get_card_num()
            suit = cards[i].get_suit()
            
            #create binary encoding for suit
            game_features[6 * i + 2] = suit == 'c' 
            game_features[6 * i + 3] = suit == 'd'
            game_features[6 * i + 4] = suit == 's'
            game_features[6 * i + 5] = suit == 'h'

        #player stack size
        game_features[42] = self.stack

        return game_features

    def gen_action_features(self, action, game_state):

        """ This method generates a set of features from a player action. """

        #create binary encoding for action type
        action_features = 7 * [0]

        if action[0] == 'check': action_features[0] = 1
        elif action[0] == 'fold': action_features[1] = 1
        elif action[0] == 'call': action_features[2] = 1
        elif action[0] == 'raise' or action[0] == 'bet':
            action_features[3] = 1
            action_features[4] = action[1]    #raise to amount
            action_features[5] = action[1] - max(game_state.current_bets)    #raise by amount
            action_features[6] = action_features[5] / sum(game_state.bets + game_state.current_bets)    #proportion of raise by to pot size
        else: raise Exception('Invalid action.')

        return action_features
#!/usr/bin/env python3

import random

import numpy as np


class Player(object):

    """
    This class keeps a player's current stack size and bankroll and is primarily responsible for
    receiving GameStates and returning actions.
    """

    def __init__(self, name, bankroll, n_raises, memory, r_factor=None, reg=None):
        """ 
        Parameters

        name - player's name (string)
        bankroll- player's net worth (int)
        n_raises - number of raise choices player has, all-in always included (int)
        memory - player forgets oldest stored features/labels that exceed memory in quantity (int)
        r_factor - each raise choice is r_factor times the next largest raise choice (float)
        reg - machine learning regressor, must be sklearn or implement 'fit' and 'predict'
        """

        self.name = name  # for distinction from other players
        self.fit = False  # True when self.regressor has been fit
        self.bankroll = bankroll  # total wealth of player
        self.stack = 0  # chips that player has on table
        self.features = []  # features associated with each game_state seen
        self.stacks = []  # stack size at each time that features are recorded
        self.labels = []  # result of each hand played
        self.memory = memory  # max number of features, stacks, and labels to store
        self.regressor = reg  # machine learning regressor which predicts return on action

        self.train = True  # player will not update regressor if self.train is False

        if r_factor == None and n_raises != 1:
            raise Exception('Must set \'r_factor\' when \'n_raises\ is not 1.')
        if r_factor <= 0 or r_factor >= 1:
            raise Exception('r_factor must be between 0 and 1, exclusive.')

        # generate logrithmically distributed raise choices, as multiples of stack
        self.r_choices = [1]
        for i in range(n_raises - 1):
            self.r_choices = [self.r_choices[0] * r_factor] + self.r_choices

    def buy_chips(self, new_stack):
        """ This method moves chips to player's bankroll such that player's stack is 'new_stack'. """

        if new_stack > self.bankroll + self.stack:
            return False  # player cannot buy chips

        if new_stack < self.stack:
            raise Exception('Requested stack is smaller than old stack.')

        move = new_stack - self.stack
        self.bankroll -= move
        self.stack += move

        return True

    def cash_out(self):
        self.bankroll += self.stack
        self.stack = 0

    def act(self, game_state, vocal=False):
        """ 
        Accepts a game_state object and returns an action in the form (action_string, amount). 
        Valid action_strings are fold, check, call, raise, and bet.
        """

        game_features = self.gen_game_features(game_state)
        all_actions = self.all_actions(game_state)

        # if player has not yet been trained
        if not self.fit:
            action = random.choice(all_actions)  # take a random action

        else:
            # determine best action
            all_features = []
            for a in all_actions:
                all_features.append(
                    game_features + self.gen_action_features(a, game_state))
            p_return = self.regressor.predict(all_features)
            action = all_actions[np.argmax(p_return)]

        # store action features
        action_features = self.gen_action_features(action, game_state)

        if self.train:
            self.stacks.append(self.stack)
            self.features.append(game_features + action_features)

        if (vocal and self.name == "User"):
            print("Possible moves: \n" + str(all_actions))
            pos_move = int(
                input("Enter number to select which move to play: "))
            action = all_actions[pos_move]
            print("Action: " + str(action))
        return action

    def remove_chips(self, amount):
        if amount > self.stack:
            raise Exception('Requested chips is greater than stack size.')
        if type(amount) != int:
            raise Exception('Must remove integer number of chips.')
        self.stack -= amount

    def add_chips(self, amount):
        if type(amount) != int:
            raise Exception('Must add integer number of chips.')
        self.stack += amount

    def end_hand(self):
        """
        This method discards data older than 'self.memory' and updates 'self.labels' with 
        the change from stack size at each feature generation.
        """

        for i in range(len(self.labels), len(self.features)):
            self.labels.append(self.stack - self.stacks[i])

        self.features = self.features[-self.memory:]
        self.stacks = self.stacks[-self.memory:]
        self.labels = self.labels[-self.memory:]

    def train_player(self):
        """ 
        This method trains the player's regressor using the set of gathered features and labels
        in ordered to predict the outcome of any given action.
        """

        if not self.train:
            return

        self.regressor.fit(self.features, self.labels)
        self.fit = True

    def all_actions(self, game_state):
        """ This method accepts the dictionary game_state and returns the set of all possible actions. """

        to_call = game_state.to_call  # amount necessary to call
        min_raise = game_state.min_raise  # new total bet amount necessary to raise
        current_bets = game_state.current_bets
        my_current_bet = current_bets[game_state.actor]
        # maximum bet player could have in pot, including chips already in pot
        max_bet = (self.stack + my_current_bet) // 5

        actions = []  # set of all possible actions

        if to_call > self.stack:  # player cannot match entire bet
            actions.append(('call',))
            actions.append(('fold',))
            return actions

        if max_bet < min_raise:  # player has enough chips to call but not to raise
            if to_call == 0:
                actions.append(('check',))
            else:
                actions.append(('call',))
                actions.append(('fold',))
            return actions

        # add eligible raise choices to actions
        # raise actions include a raise to amount, not a raise by amount
        for r in self.r_choices:
            amount = int(self.stack * r)
            if amount >= min_raise and amount <= max_bet:
                actions.append(('raise', amount))

        # player has enough chips to raise
        if to_call == 0:
            actions.append(('check',))
        else:
            actions.append(('call',))
            actions.append(('fold',))

        return actions

    def gen_game_features(self, game_state):
        """ 
        This method generates a set of features from a game_state and independently of the
        action a player takes. 
        """

        game_features = 43 * [0]

        hold_cards = sorted(self.cards)
        table_cards = sorted(game_state.cards)

        # add number and suit of each card to features
        cards = hold_cards + table_cards
        for i in range(len(cards)):
            game_features[6 * i] = 1  # ith card exists
            game_features[6 * i + 1] = cards[i].get_card_num()
            suit = cards[i].get_suit()

            # create binary encoding for suit
            game_features[6 * i + 2] = suit == 'c'
            game_features[6 * i + 3] = suit == 'd'
            game_features[6 * i + 4] = suit == 's'
            game_features[6 * i + 5] = suit == 'h'

        # player stack size
        game_features[42] = self.stack

        return game_features

    def gen_action_features(self, action, game_state):
        """ This method generates a set of features from a player action. """

        # create binary encoding for action type
        action_features = 7 * [0]

        if action[0] == 'check':
            action_features[0] = 1
        elif action[0] == 'fold':
            action_features[1] = 1
        elif action[0] == 'call':
            action_features[2] = 1
        elif action[0] == 'raise' or action[0] == 'bet':
            action_features[3] = 1
            action_features[4] = action[1]  # raise to amount
            action_features[5] = action[1] - \
                max(game_state.current_bets)  # raise by amount
            # proportion of raise by to pot size
            action_features[6] = action_features[5] / \
                sum(game_state.bets + game_state.current_bets)
        else:
            raise Exception('Invalid action.')

        return action_features

    def take_hole_cards(self, cards): self.cards = cards

    def stop_training(self): self.train = False

    def start_training(self): self.train = True

    def show(self): return self.cards

    def get_stack(self): return self.stack

    def get_bankroll(self): return self.bankroll

    def get_name(self): return self.name

    def get_raise_choices(self): return self.r_choices[:]

    def get_features(self): return self.features[:]

    def get_labels(self): return self.labels[:]

    def set_bankroll(self, amount): self.bankroll = amount

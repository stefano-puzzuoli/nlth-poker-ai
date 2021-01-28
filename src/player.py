import random
import numpy as np

class Player:

    def __init__(self, name, bankroll, n_raises, memory, r_factor=None, reg=None):

        
        self.name = name            
        self.fit = False            
        self.bankroll = bankroll    
        self.stack = 0             
        self.features = []          
        self.stacks = []            
        self.labels = []            
        self.memory = memory        
        self.regressor = reg        
        
        self.train = True           

        if r_factor == None and n_raises != 1:
            raise Exception('Must set \'r_factor\' when \'n_raises\ is not 1.')
        if r_factor <= 0 or r_factor >= 1: raise Exception('r_factor must be between 0 and 1, exclusive.')

        self.r_choices = [1]
        for i in range(n_raises - 1):
            self.r_choices = [self.r_choices[0] * r_factor] + self.r_choices

    def buy_chips(self, new_stack):


        if new_stack > self.bankroll + self.stack: return False    

        if new_stack < self.stack: raise Exception('Requested stack is smaller than old stack.')

        move = new_stack - self.stack
        self.bankroll -= move
        self.stack += move

        return True

    def cash_out(self):
        self.bankroll += self.stack
        self.stack = 0

    def act(self, game_state, vocal=False):


        game_features = self.gen_game_features(game_state)
        all_actions = self.all_actions(game_state)

        if not self.fit: action = random.choice(all_actions)    

        else:
            all_features = []
            for a in all_actions: all_features.append(game_features + self.gen_action_features(a, game_state))
            p_return = self.regressor.predict(all_features)
            action = all_actions[np.argmax(p_return)]



        action_features = self.gen_action_features(action, game_state)  

        if self.train: 
            self.stacks.append(self.stack)
            self.features.append(game_features + action_features)

        
        if (vocal and self.name == "User"):
            print("Possible moves: \n" + str(all_actions))
            pos_move = int(input("Enter number to select which move to play: "))
            action =  all_actions[pos_move]
            print("Action: " + str(action))  
        return action      

    def remove_chips(self, amount):
        if amount > self.stack: raise Exception('Requested chips is greater than stack size.')
        if type(amount) != int: raise Exception('Must remove integer number of chips.')
        self.stack -= amount

    def add_chips(self, amount): 
        if type(amount) != int: raise Exception('Must add integer number of chips.')
        self.stack += amount

    def end_hand(self): 

        for i in range(len(self.labels), len(self.features)):
            self.labels.append(self.stack - self.stacks[i])

        self.features = self.features[-self.memory:]
        self.stacks = self.stacks[-self.memory:]
        self.labels = self.labels[-self.memory:]

    def train_player(self):

        
        if not self.train: return

        self.regressor.fit(self.features, self.labels)
        self.fit = True

    def all_actions(self, game_state):
        

        to_call = game_state.to_call    
        min_raise = game_state.min_raise    
        current_bets = game_state.currBets
        my_current_bet = current_bets[game_state.actor]
        max_bet = (self.stack + my_current_bet) // 5  

        actions = []    

        if to_call > self.stack:   
            actions.append(('call',))
            actions.append(('fold',))
            return actions
            
        if max_bet < min_raise:    
            if to_call == 0: actions.append(('check',))
            else: 
                actions.append(('call',))
                actions.append(('fold',))
            return actions


        for r in self.r_choices:
            amount = int(self.stack * r) 
            if amount >= min_raise and amount <= max_bet: actions.append(('raise', amount))

        if to_call == 0: actions.append(('check',))
        else:
            actions.append(('call',))
            actions.append(('fold',))
        
        return actions

    def gen_game_features(self, game_state): raise Exception('This method must be implemented in an inherited class.')

    def gen_action_features(self, action, game_state): raise Exception('This method must be implemented in an inherited class.')

    def take_hole_cards(self, cards): self._cards = cards

    def stop_training(self): self.train = False

    def start_training(self): self.train = True

    def show(self): return self._cards

    def get_stack(self): return self.stack

    def get_bankroll(self): return self.bankroll

    def get_name(self): return self.name
    
    def get_raise_choices(self): return self.r_choices[:]

    def get_features(self): return self.features[:]

    def get_labels(self): return self.labels[:]

    def set_bankroll(self, amount): self.bankroll = amount
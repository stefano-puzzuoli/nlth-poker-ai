from random import shuffle
from .player import Player
from .card import Card
from .evaluator.evaluator import Evaluator
from .gamestate import GameState

class Table:

    """
    This class is primarily responsible for core holdem simulation logic. Basic usage consists of 
    adding players via add_player() and simulating a single hand via play_hand(). For simplicity, betting takes place
    with integer number of chips with uniform value.
    """

    def __init__(self, small_bind, big_blind, max_buy_in):

        """ Constructor accepts  blinds and maximum table buy in as integers. """
        
        self.players = []  #players at the table
        self.playing = []  #players who are not bankrupt
        self.sit_out = []   #players who have gone bankrupt
        self.dealer = 0    #position of dealer in self.playing
        self.eval = Evaluator()

        if type(small_bind) != int or type(big_blind) != int or type(max_buy_in) != int:
            raise Exception('Parameters must be integer number of chips.')
        self.small_bind = small_bind
        self.big_blind = big_blind
        self.max_buy_in = max_buy_in

    def add_player(self, player):

        self.sit_out.append(player)
        self.players.append(player)

    def play_hand(self, vocal=False):

        """ 
        This method simulates one hand between added players. Narrates hand if vocal is True.
        Returns False if unable to play hand. 
        """

        self.vocal = vocal

        #add players to hand who are eligible to play
        for player in self.sit_out[:]:
            if player.get_stack() >= self.big_blind:
                if player.get_stack() > self.max_buy_in: 
                    raise Exception('Player\'s stack is greater than maximum buy in.')
                self.playing.append(player)
                self.sit_out.remove(player)

        if len(self.playing) <= 1: return False
            
        #reset table game state before hand
        self.state = GameState(self.playing)
    
        #commence simulation
        self.gen_deck()
        self.deal_hole_cards()
        self.pre_flop(vocal)
        self.flip(3, vocal)
        self.flip(1, vocal)
        self.flip(1, vocal)
        self.pay_winners()
        for player in self.playing: player.end_hand()

        #find next dealer
        dealer_position = (self.dealer + 1) % self.state.num_players
        while self.playing[dealer_position].get_stack() < self.big_blind: 
            dealer_position = (dealer_position + 1) % self.state.num_players
        dealer = self.playing[dealer_position]

        #remove players who have gone bankrupt
        for player in self.playing[:]:
            if player.get_stack() < self.big_blind:
                self.playing.remove(player)
                self.sit_out.append(player)

        #move dealer chip 
        self.dealer = 0
        while self.playing[self.dealer] != dealer: self.dealer = (self.dealer + 1) % self.state.num_players

        if vocal: print()
        return True

    def gen_deck(self):

        self.deck = []
        for s in ['c', 'd', 'h', 's']:
            for i in range(2,15):
                self.deck.append(Card(i,s))
        shuffle(self.deck)
 
    def deal_hole_cards(self):

        """ This method gives each player their starting cards at the beginning of the hand. """

        for player in self.playing:
            player.take_hole_cards((self.deck[0],self.deck[1]))
            if self.vocal: print(player.get_name() + '(' + str(player.get_stack()) + ')', 'dealt', self.deck[0], 'and', self.deck[1])
            self.deck = self.deck[2:]
        if self.vocal: print()

    def pre_flop(self, vocal=False):

        """ This method posts the blinds and commences betting. """

        self.state.min_raise = 2 * self.big_blind    #minimum first raise before flop is 2 x Big Blind

        sb_position = (self.dealer + 1) % self.state.num_players    #small blind position
        bb_position = (self.dealer + 2) % self.state.num_players    #big blind position
        self.state.actor = (self.dealer + 3) % self.state.num_players    #first player to act

        #Heads-Up (1v1) has different rules prelop
        if self.state.num_players == 2:    
            sb_position = self.dealer    
            bb_position = (self.dealer + 1) % self.state.num_players
            self.state.actor = self.dealer   

        #post blinds
        self.state.current_bets[sb_position] += self.small_bind
        self.playing[sb_position].remove_chips(self.small_bind)
        if self.vocal:print(self.playing[sb_position].get_name(), 'posts small blind of', self.small_bind)
        self.state.current_bets[bb_position] += self.big_blind
        self.playing[bb_position].remove_chips(self.big_blind)
        if self.vocal: print(self.playing[bb_position].get_name(), 'posts big blind of', self.big_blind)

        self.open_betting(vocal)
        if self.vocal: print()

    def flip(self, num_cards, vocal=False):  

        """ This method flips num_cards cards from deck to be seen by players and then commences betting. """

        if len(self.state.folded) + 1 == self.state.num_players: return    #all players but one have folded

        self.state.min_raise = self.big_blind    #minimum first bet after the flop is Big Blind

        #flip num_cards
        self.state.cards += self.deck[:num_cards]
        if self.vocal: print([str(c) for c in self.state.cards])
        self.deck = self.deck[num_cards:]
        
        self.state.actor = (self.dealer + 1) % self.state.num_players    #first actor is player after dealer
        
        self.open_betting(vocal)
        if self.vocal: print()

    def pay_winners(self):

        """ This method distributes the pot to the winner(s). """

        board = [card.to_int() for card in self.state.cards]
        
        #evaluate rank of hand for each player
        ranks = {}
        for player in self.playing:
            if not board: rank = -1    #all players but one have folded before flop
            else: rank = self.eval.evaluate(board, [player.show()[0].to_int(), player.show()[1].to_int()])
            ranks[player] = rank

        n = 0
        while sum(self.state.bets) > 0:    #to handle n side pots

            #get rank of best hand and bet of each player who is eligible to win sub pot
            min_live_bet = None    #bet that any eligible player has in current sub pot
            min_rank = None
            eligible_winners = []
            for i in range(self.state.num_players):
                if not i in self.state.folded and self.state.bets[i] != 0:    #if player hasnt folded and has stake in current sub pot
                    if min_live_bet == None: min_live_bet = self.state.bets[i]
                    else: min_live_bet = min(min_live_bet, self.state.bets[i])
                    player = self.playing[i]
                    eligible_winners.append(player)
                    if min_rank == None: min_rank = ranks[player]
                    else: min_rank = min(min_rank, ranks[player])

            #create sub pot by adding contributions of its members
            winners = [player for player in eligible_winners if ranks[player] == min_rank]
            sub_pot = 0
            for i in range(self.state.num_players):
                contribution = min(min_live_bet, self.state.bets[i])
                self.state.bets[i] -= contribution
                sub_pot += contribution


            #pay winners
            winnings = int(float(sub_pot) / len(winners))
            for winner in winners:
                winner.add_chips(winnings)
                sub_pot -= winnings
                if self.vocal:
                    if min_rank == -1:    #everyone else folded
                        print(winner.get_name(), 'wins', winnings)
                    else:   
                        if n == 0: print(winner.get_name(), 'wins', winnings, 'from main pot')
                        if n > 0: print(winner.get_name(), 'wins', winnings, 'from side pot')

            #give odd chips to player in earliest position
            if sub_pot > 0:
                actor = (self.dealer + 1) % self.state.num_players
                while sub_pot > 0:
                    player = self.playing[actor]
                    if player in winners:
                        player.add_chips(sub_pot)
                        if self.vocal: print(player.get_name(), 'wins', sub_pot, 'odd chips')
                        sub_pot = 0
                    actor = (actor + 1) % self.state.num_players

            n += 1

    def open_betting(self, vocal=False): 

        """ The method starts a round of betting. """

        last_to_raise = self.state.actor    #so that action ends when everyone checks

        #main betting loop
        t = 0
        while True: 
            t += 1      

            actor = self.state.actor

            if actor == last_to_raise and t > 1: break    #break if last raising player has been reached
            
            #break if no further calls are possible
            not_allin_or_fold = []
            for i in range(self.state.num_players):
                if i not in self.state.folded and i not in self.state.all_in: not_allin_or_fold.append(i)
            if len(not_allin_or_fold) == 0: break    #break if all players are folded or all-in
            #break if last player's raise cannot be matched
            if len(not_allin_or_fold) == 1 and self.state.current_bets[not_allin_or_fold[0]] == max(self.state.current_bets): break    

            #skip player if player folded or player is all in
            if actor in self.state.folded or actor in self.state.all_in: 
                self.state.actor = (actor + 1) % self.state.num_players 
                continue

            self.state.to_call = max(self.state.current_bets) - self.state.current_bets[actor]    #player must call maximum bet to call

            #request player action and parse action
            action = self.playing[actor].act(self.state, vocal)
            self.parse_action(action)
            if action[0] == 'raise': last_to_raise = actor
            
            self.state.actor = (actor + 1) % self.state.num_players  #move to next player

        #return uncalled chips to raiser
        unique_bets = sorted(set(self.state.current_bets))
        max_bet = unique_bets[-1]
        if len(unique_bets) >= 2: below_max = unique_bets[-2]
        if len([bet for bet in self.state.current_bets if bet==max_bet]) == 1:
            for i in range(self.state.num_players):
                if self.state.current_bets[i] == max_bet:
                    self.state.current_bets[i] = below_max
                    player = self.playing[i]
                    player.add_chips(max_bet - below_max)
                    if self.vocal: print(max_bet - below_max, 'uncalled chips return to', player.get_name())

        self.state.actor = None    #action has closed
        
        #add bets of current round to bets and flush current_bets and num_raises
        for i in range(len(self.state.current_bets)): 
            self.state.bets[i] += self.state.current_bets[i]    
            self.state.current_bets[i] = 0
            self.state.num_raises[i] = 0

    def parse_action(self, action):

        """ 
        This method accepts a tuple of the form (action string, amount) or (action string,) and changes
        the GameState, self.state, appropriately.
        """
        actor = self.state.actor
        player = self.playing[actor]
        maximum = max(self.state.current_bets)    #largest contribution that any player has in current pot
        current_bet = self.state.current_bets[actor]

        if action[0] == 'check':
            if current_bet < maximum: raise Exception('Player must call to remain in the pot.')
            if self.vocal: print(player.get_name(), 'checks.')
        
        elif action[0] == 'fold': 
            self.state.folded.append(actor)
            if self.vocal: print(player.get_name(), 'folds.') 
        
        elif action[0] == 'call': 
            to_call = self.state.to_call
            if to_call == 0: raise Exception('Player called a bet of 0 chips. Did you mean to check?')
            stack = player.get_stack()
            if stack <= to_call:    #player has all-in called
                self.state.current_bets[actor] += stack
                player.remove_chips(stack)
                if self.vocal: print(player.get_name(), 'all-in calls with', stack)
                self.state.all_in.append(actor)
            else:
                self.state.current_bets[actor] = maximum
                player.remove_chips(maximum - current_bet)
                if self.vocal: print(player.get_name(), 'calls', maximum - current_bet)
        
        elif action[0] == 'raise' or action[0] == 'bet':    #raising is interpreted as "raise to" a a new total bet
            raise_to = action[1]    #new total bet of player
            raise_by = raise_to - maximum    #change in maximum bet in pot
            # if action[0] == 'bet' and maximum > 0: raise Exception('Cannot bet when pot has been opened. Did you mean to raise?')
            # if action[0] == 'raise' and maximum == 0: raise Exception('Cannot raise when pot is unopened. Did you mean to bet?')
            if raise_to < self.state.min_raise: raise Exception('Raise amount is less than minimum raise.')
            self.state.min_raise = raise_to + raise_by    #player must raise by twice as much as last raise
            self.state.current_bets[actor] = raise_to
            player.remove_chips(raise_to - current_bet)
            self.state.num_raises[actor] += 1
            all_in  = player.get_stack() == 0
            if all_in: self.state.all_in.append(actor)
            if self.vocal: 
                if not all_in: print(player.get_name(), 'raises', raise_by, 'to', raise_to)
                else: print(player.get_name(), 'raises all-in', raise_by, 'to', raise_to)
        
        else: raise Exception('Invalid player action.')

    def get_playing(self): return self.playing[:]

    def get_sit_out(self): return self.sit_out[:]

    def get_players(self): return self.players[:]

    def get_params(self): return (self.small_bind, self.big_blind, self.max_buy_in)

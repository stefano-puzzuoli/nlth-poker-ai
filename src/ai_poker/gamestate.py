#!/usr/bin/env python3

class GameState(object):

    """This class is responisble for holding all game data that is accessible to Players"""

    def __init__(self, players):

        #amount of chips necessary to call without going all-in
        self.to_call = None                           
        
        #minimum raise size, player must increase bet to minRaise to raise
        self.min_raise = None                         
        
        #number of players in hand
        self.num_players = len(players)               
        
        #total contribution of each player to completed betting rounds
        #by position of player in self._playing  
        #sum of bets is total pot excluding current betting round
        self.bets = [0 for p in players]       
        
        #total contribution of each player to pot of current betting round
        #sum of currBets is total pot of current round
        #sum of bets and currBets is total pot
        self.current_bets = [0 for p in players]   
        
        #list of positions where players have folded
        self.folded = []
        
        #list of positions where players are all-in
        self.all_in = []                                    
        
        #face up community cards
        self.cards = []                              
        
        #index of player who is currently acting in self._playing
        self.actor = None                             

        #number of raises this round by position of player
        self.num_raises = [0 for p in players]
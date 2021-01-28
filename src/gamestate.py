class GameState:

    def __init__(self, players):

        self.to_call = None                           
        
        self.min_raise = None                         
        
        self.num_players = len(players)               
        
        self.bets = [0 for p in players]       

        self.current_bets = [0 for p in players]   
        
        self.folded = []
        
        self.all_in = []                                    
        
        self.cards = []                              
        
        self.actor = None                             

        self.num_raises = [0 for p in players]
from evaluator.card import Card as ECard

class Card:
    
    n_enumerator = {'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    suits = ['c', 'd', 's', 'h']

    def __init__(self, card_num, suit):
        if type(card_num) == int:
            if card_num < 2 or card_num > 14: raise Exception('Card number must be between 2 and 14 (inclusive).')
            self._card_num = card_num
            for k in self.n_enumerator:
                if self.n_enumerator[k] == card_num: self._card_num = k
        elif type(card_num) == str:
            if card_num.upper() not in self.n_enumerator: raise Exception("Card letter must be \'T\', \'J\', \'Q\', \'K\', or \'A\'.")
            self._card_num = card_num.upper()
        else: raise Exception('Card number/letter must be number or string.')

        if suit.lower() not in self.suits: raise Exception("Invalid suit. Valid suits are \'c\', \'d\', \'s\', and \'h\'.")
        self._suit = suit.lower()

    def getCardNum(self):
        
        if self._card_num in self.n_enumerator: return self.n_enumerator[self._card_num]
        return self._card_num

    def getSuit(self): return self._suit

    def toInt(self): return ECard.new(str(self))

    def __lt__(self, other): return self.getCardNum() < other.getCardNum()

    def __str__(self): return str(self._card_num) + self._suit

        




        



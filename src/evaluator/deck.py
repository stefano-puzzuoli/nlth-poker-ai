from random import shuffle
from card import Card

class Deck:
    complete_deck = []

    def __init__(self):
        self.shuffle()

    def shuffle(self):
        # and then shuffle
        self.cards = Deck.getCompleteDeck()
        shuffle(self.cards)

    def pick(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.pick())
        return cards

    def __str__(self):
        return Card.print_unicode_cards(self.cards)

    @staticmethod
    def getCompleteDeck():
        if Deck.complete_deck:
            return list(Deck.complete_deck)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit,val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                Deck.complete_deck.append(Card.new(rank + suit))

        return list(Deck.complete_deck)
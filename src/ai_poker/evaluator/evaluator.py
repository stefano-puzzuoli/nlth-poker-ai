
import itertools
from ai_poker.evaluator.card_service import CardService
from ai_poker.evaluator.deck import Deck
from ai_poker.evaluator.lookup import LookupTable

class Evaluator(object):

    def __init__(self):

        self.table = LookupTable()
        
        self.hand_map = {
            5 : self.five,
            6 : self.six,
            7 : self.seven
        }

    def evaluate(self, cards, board):
        all_cards = cards + board
        return self.hand_map[len(all_cards)](all_cards)

    def five(self, cards):
        if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000:
            handOR = (cards[0] | cards[1] | cards[2] | cards[3] | cards[4]) >> 16
            prime = CardService.prime_product_from_rbits(handOR)
            return self.table.lookup_flush[prime]

        else:
            prime = CardService.prime_product_from_hand(cards)
            return self.table.lookup_unsuited[prime]

    def six(self, cards):
        minimum = LookupTable.h_card

        five_card_combos = itertools.combinations(cards, 5)
        for combo in five_card_combos:

            score = self.five(combo)
            if score < minimum:
                minimum = score

        return minimum

    def seven(self, cards):
        """
        Performs five_card_eval() on all (7 choose 5) = 21 subsets
        of 5 cards in the set of 7 to determine the best ranking, 
        and returns this ranking.
        """
        minimum = LookupTable.h_card

        five_card_combos = itertools.combinations(cards, 5)
        for combo in five_card_combos:
            
            score = self.five(combo)
            if score < minimum:
                minimum = score

        return minimum

    def get_hand_rank(self, hr):
        if hr >= 0 and hr < LookupTable.s_flush:
            return LookupTable.hand_rank[LookupTable.s_flush]
        elif hr <= LookupTable.four_kind:
            return LookupTable.hand_rank[LookupTable.four_kind]
        elif hr <= LookupTable.f_house:
            return LookupTable.hand_rank[LookupTable.f_house]
        elif hr <= LookupTable.flush:
            return LookupTable.hand_rank[LookupTable.flush]
        elif hr <= LookupTable.straight:
            return LookupTable.hand_rank[LookupTable.straight]
        elif hr <= LookupTable.three_kind:
            return LookupTable.hand_rank[LookupTable.three_kind]
        elif hr <= LookupTable.two_pair:
            return LookupTable.hand_rank[LookupTable.two_pair]
        elif hr <= LookupTable.pair:
            return LookupTable.hand_rank[LookupTable.pair]
        elif hr <= LookupTable.h_card:
            return LookupTable.hand_rank[LookupTable.h_card]
        else:
            raise Exception("Inavlid hand rank, cannot return rank class")

    def to_string(self, class_int):
        return LookupTable.rank_string[class_int]

    def get_rank_percentage(self, hand_rank):

        return float(hand_rank) / float(LookupTable.h_card)

    def hand_summary(self, board, hands):
        assert len(board) == 5, "Invalid board length"
        for h in hands:
            assert len(h) == 2, "Inavlid hand length"

        line_length = 10
        game_stages = ["FLOP", "TURN", "RIVER"]

        for i in range(len(game_stages)):
            line = ("=" * line_length) + " %s " + ("=" * line_length) 
            print(line % game_stages[i])
            
            best_rank = 7463 
            winners = []
            for player, h in enumerate(hands):
                rank = self.evaluate(h, board[:(i + 3)])
                hand_rank = self.get_hand_rank(rank)
                rank_string = self.to_string(hand_rank)
                percentage = 1.0 - self.get_rank_percentage(rank) 
                print("Player %d hand = %s, percentage rank among all hands = %f" % (
                    player + 1, rank_string, percentage))

                if rank == best_rank:
                    winners.append(player)
                    best_rank = rank
                elif rank < best_rank:
                    winners = [player]
                    best_rank = rank

            if i != game_stages.index("RIVER"):
                if len(winners) == 1:
                    print("Player %d hand is currently winning.\n" % (winners[0] + 1,))
                else:
                    print("Players %s are tied for the lead.\n" % [x + 1 for x in winners])
            else:
                print
                print(("=" * line_length) + " HAND OVER " + ("=" * line_length))
                if len(winners) == 1:
                    print("Player %d is the winner with a %s\n" % (winners[0] + 1, 
                        self.to_string(self.get_hand_rank(self.evaluate(hands[winners[0]], board)))))
                else:
                    print("Players %s tied for the win with a %s\n" % (winners, 
                        self.to_string(self.get_hand_rank(self.evaluate(hands[winners[0]], board)))))
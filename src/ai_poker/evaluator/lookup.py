import itertools
from ai_poker.evaluator.card import Card

class LookupTable(object):
    s_flush  = 10
    four_kind  = 166
    f_house      = 322 
    flush           = 1599
    straight        = 1609
    three_kind = 2467
    two_pair        = 3325
    pair            = 6185
    h_card       = 7462

    hand_rank = {
        s_flush: 1,
        four_kind: 2,
        f_house: 3,
        flush: 4,
        straight: 5,
        three_kind: 6,
        two_pair: 7,
        pair: 8,
        h_card: 9
    }

    rank_string = {
        1 : "Straight Flush",
        2 : "Four of a Kind",
        3 : "Full House",
        4 : "Flush",
        5 : "Straight",
        6 : "Three of a Kind",
        7 : "Two Pair",
        8 : "Pair",
        9 : "High Card"
    }

    def __init__(self):
        self.lookup_flush = {}
        self.lookup_unsuited = {}

        self.flushes()  
        self.multiples()

    def flushes(self):
        s_flushes = [
            7936,
            3968,
            1984,
            992,
            496,
            248, 
            124, 
            62, 
            31, 
            4111 
        ]

        flushes = []
        gen_bit = self.get_next_lex_bit(int('0b11111', 2))

        for i in range(1277 + len(s_flushes) - 1): 
            f = next(gen_bit)
            not_sf = True
            for sf in s_flushes:
                if not f ^ sf:
                    not_sf = False

            if not_sf:
                flushes.append(f)

        flushes.reverse()
        rank = 1
        for sf in s_flushes:
            prime_product = Card.prime_product_from_rbits(sf)
            self.lookup_flush[prime_product] = rank
            rank += 1

        rank = LookupTable.f_house + 1
        for f in flushes:
            prime_product = Card.prime_product_from_rbits(f)
            self.lookup_flush[prime_product] = rank
            rank += 1

        self.striaght_and_hcards(s_flushes, flushes)

    def striaght_and_hcards(self, straights, hcards):
        rank = LookupTable.flush + 1

        for s in straights:
            prime_product = Card.prime_product_from_rbits(s)
            self.lookup_unsuited[prime_product] = rank
            rank += 1

        rank = LookupTable.pair + 1
        for h in hcards:
            prime_product = Card.prime_product_from_rbits(h)
            self.lookup_unsuited[prime_product] = rank
            rank += 1

    def multiples(self):
        reverse_ranks = list(range(len(Card.int_ranks) - 1, -1, -1))
        rank = LookupTable.s_flush + 1
        for i in reverse_ranks:
            kickers = reverse_ranks[:]
            kickers.remove(i)
            for k in kickers:
                product = Card.prime_nums[i]**4 * Card.prime_nums[k]
                self.lookup_unsuited[product] = rank
                rank += 1
        
        rank = LookupTable.four_kind + 1

        for i in reverse_ranks:

            pairranks = reverse_ranks[:]
            pairranks.remove(i)
            for pr in pairranks:
                product = Card.prime_nums[i]**3 * Card.prime_nums[pr]**2
                self.lookup_unsuited[product] = rank
                rank += 1

        rank = LookupTable.straight + 1

        for r in reverse_ranks:

            kickers = reverse_ranks[:]
            kickers.remove(r)
            gen_bit = itertools.combinations(kickers, 2)

            for kickers in gen_bit:

                c1, c2 = kickers
                product = Card.prime_nums[r]**3 * Card.prime_nums[c1] * Card.prime_nums[c2]
                self.lookup_unsuited[product] = rank
                rank += 1

        rank = LookupTable.three_kind + 1

        tpgen = itertools.combinations(reverse_ranks, 2)
        for tp in tpgen:

            pair1, pair2 = tp
            kickers = reverse_ranks[:]
            kickers.remove(pair1)
            kickers.remove(pair2)
            for kicker in kickers:

                product = Card.prime_nums[pair1]**2 * Card.prime_nums[pair2]**2 * Card.prime_nums[kicker]
                self.lookup_unsuited[product] = rank
                rank += 1

        rank = LookupTable.two_pair + 1

        for pair in reverse_ranks:

            kickers = reverse_ranks[:]
            kickers.remove(pair)
            kgen = itertools.combinations(kickers, 3)

            for kickers in kgen:

                k1, k2, k3 = kickers
                product = Card.prime_nums[pair]**2 * Card.prime_nums[k1] \
                        * Card.prime_nums[k2] * Card.prime_nums[k3]
                self.lookup_unsuited[product] = rank
                rank += 1

    def l_table_to_disk(self, table, filepath):
        with open(filepath, 'w') as f:
            for prime_prod, rank in table.iteritems():
                f.write(str(prime_prod) +","+ str(rank) + '\n')

    def get_next_lex_bit(self, bits):
        t = (bits | (bits - 1)) + 1 
        next = t | ((((t & -t) // (bits & -bits)) >> 1) - 1)  
        yield next
        while True:
            t = (next | (next - 1)) + 1 
            next = t | ((((t & -t) // (next & -next)) >> 1) - 1)
            yield next
#!/usr/bin/env python3

class CardService(object):
    string_ranks = '23456789TJQKA'
    int_ranks = range(13)
    prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    # converstion from string => int
    char_to_int_rank = dict(zip(list(string_ranks), int_ranks))
    char_to_int_rank_suit = {
        's' : 1, # spades
        'h' : 2, # hearts
        'd' : 4, # diamonds
        'c' : 8, # clubs
    }
    int_to_char_suit = 'xshxdxxxc'

    # for pretty printing
    unicode_suits = {
        1 : "♠", # spades 
        2 : "♥", # hearts
        4 : "♦", # diamonds
        8 : "♣" # clubs
    }

     # hearts and diamonds
    unicode_reds = [2, 4]

    @staticmethod
    def new(string):
        r_char = string[0]
        suit_char = string[1]
        r_int = CardService.char_to_int_rank[r_char]
        suit_int = CardService.char_to_int_rank_suit[suit_char]
        r_prime = CardService.prime_nums[r_int]

        bitrank = 1 << r_int << 16
        suit = suit_int << 12
        rank = r_int << 8

        return bitrank | suit | rank | r_prime

    @staticmethod
    def str_from_int(n):
        r_int = CardService.get_rank_int(n)
        suit_int = Card.get_suit_int(n)
        return CardService.string_ranks[r_int] + CardService.int_to_char_suit[suit_int]

    @staticmethod
    def get_rank_int(n):
        return (n >> 8) & 0xF

    @staticmethod
    def get_suit_int(n):
        return (n >> 12) & 0xF

    @staticmethod
    def get_bitr_int(n):
        return (n >> 16) & 0x1FFF

    @staticmethod
    def get_prime(n):
        return n & 0x3F

    @staticmethod
    def make_binary(s):
        bhand = []
        for c in s:
            bhand.append(CardService.new(c))
        return bhand

    @staticmethod
    def prime_product_from_hand(n):
        product = 1
        for c in n:
            product *= (c & 0xFF)

        return product

    @staticmethod
    def prime_product_from_rbits(rbits):
        product = 1
        for i in CardService.int_ranks:
            # if the ith bit is set
            if rbits & (1 << i):
                product *= CardService.prime_nums[i]

        return product

    @staticmethod
    def binary_from_int(n):
        bstr = bin(n)[2:][::-1] # chop off the 0b and THEN reverse string
        output = list("".join(["0000" +"\t"] * 7) +"0000")

        for i in range(len(bstr)):
            output[i + int(i/4)] = bstr[i]

        # output the string to console
        output.reverse()
        return "".join(output)

    @staticmethod
    def int_to_unicode(n):
        
        color = False
        try:
            from termcolor import colored
            ### for mac, linux: http://pypi.python.org/pypi/termcolor
            ### can use for windows: http://pypi.python.org/pypi/colorama
            color = True
        except ImportError: 
            pass

        # suit and rank
        suit_int = CardService.get_suit_int(n)
        r_int = CardService.get_rank_int(n)

        # if we need to color red
        s = CardService.unicode_suits[suit_int]
        if color and suit_int in CardService.unicode_reds:
            s = colored(s, "red")

        r = CardService.string_ranks[r_int]

        return " [ " +r+ " " + s + " ] "

    @staticmethod
    def print_unicode(n):
        print(CardService.int_to_unicode(n))

    @staticmethod
    def print_unicode_cards(n):
        output = " "
        for i in range(len(n)):
            c = n[i]
            if i != len(n) - 1:
                output += CardService.int_to_unicode(c) + ","
            else:
                output += CardService.int_to_unicode(c) + " "
    
        print(output)

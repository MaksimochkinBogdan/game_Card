# class Game_machine:
#     def __init__(self):
#         self.handsize = 6


#         self.winner = None

# game = Game_machine()
# print(game.__dict__)

# for n in range(2, 5):
#     count = 0
#     for k in range(2,n):
#             count += 1

# print(count)

class Deck:
    def __init__(self, cards):
        self.cards = cards

class Table:
    def __init__(self, deck: Deck):
        self.deck = deck

deck = Deck(1)
print(deck.__dict__)

t = Table(deck)
print(t.__dict__)

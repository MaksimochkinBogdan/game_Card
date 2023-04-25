
import random

VALUES = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A') # ЗНАЧЕНИЕ
SUITS = ('Spades', 'Clubs', 'Diamonds', 'Hearts') # МАСТЬ
SUITS_UNI = {
    'Spades': '♠',
    'Clubs': '♣',
    'Diamonds': '♦',
    'Hearts': '♥'
}                                                 # ОДНА ИЗ МАСТЕЙ









class Card:
    def __init__(self, value, suit):
        self.value = value # ЗНАЧЕНИЕ КАРТЫ
        self.suit = suit # МАСТЬ КАРТЫ

    def equal_suit(self, other_card):           # Проверяет одинаковая ли масть у карт
        return self.suit == other_card.suit

    def __gt__(self, other_card):                                        # Значение карты БОЛЬШЕ
        if self.value > other_card.value:
            return SUITS.index(self.suit) > SUITS.index(other_card.suit)
        return VALUES.index(self.value) > VALUES.index(other_card.value)

    def __lt__(self, other_card):                                        # Значение карты МЕНЬШЕ
        if self.value < other_card.value:
            return SUITS.index(self.suit) < SUITS.index(other_card.suit)
        return VALUES.index(self.value) < VALUES.index(other_card.value)

    def __str__(self):
        return self.__repr__ # return f"{self.value}{SUITS_UNI[self.suit]}" # выводит значение в формате ЗНАЧЕНИЕ МАСТЬ

    def __repr__(self):
        return f"{self.value}{SUITS_UNI[self.suit]}" # выводит значение в формате ЗНАЧЕНИЕ МАСТЬ







# создадим колоду из 52 карт и реализуем все методы:
class Deck:
    def __init__(self, cards=None):
        # Список Карт в Колоде. Каждый элемент списка - объект класса Card
        if cards:
            self.cards = cards
        else:
            self.cards = [Card(v, s) for v in VALUES for s in SUITS] # Список Карт в Колоде. Каждый элемент списка - объект класса Card

    def show(self): # отображает все карты в колоде в формате deck[2]: 3♠, 10♦
        return f"deck[{self.cards}] {',' .join([str(card) for card in self.cards])}"

    def __str__(self):
        return f"deck[{self.cards}] {',' .join([str(card) for card in self.cards])}"

    def draw(self, x): # возвращает Х карт из колоды
        hand = self.cards[:x] # взяли в руки карты сверху колоды
        self.cards = self.cards[x:] # то что осталось в колоде
        return hand

    def draw_all(self): # возвращает все карты из колоды
        hand = self.cards[:]
        self.cards = []
        return hand

    def clear(self):
        self.cards = []

    def add(self, cards: list[Card]):
        self.cards = self.cards + cards

    def shuffle(self):
        random.shuffle(self.cards)

    def __getitem__ (self, index):
        return self.cards[index]









class Player:
    def __init__(self, name, hand: list[Card]):
        self.name = name
        self.hand = hand

    def handsiza(self):
        return len(self.hand)

    def make_move(self, table: Deck):

        move_card = None # Ход Картой
        if table.cards: # Карты на столе
            values_on_table = set([v.value for v in table.cards])
            for v in values_on_table:
                for c in self.hand:
                    if c.value == v:
                        move_card = c
                        break
                if move_card:
                    break
            if not move_card:
                print("Бито")
                table.clear()
        else:
            if self.hand:
                move_card = min(self.hand)
            else:
                return False


        if move_card:
            print(f'{self.name}| {self.hand}')
            print(f'{self.name} играет {move_card}')
            self.remove_card(move_card)
            table.add([move_card])
            return True
        else:
            return False

        # Если сможет сходить - True, если нет - False







class Game_machine:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.handsize = 6
        self.player1 = Player('Игрок1', self.deck.draw(self.hadsize))
        self.player2 = Player('Игрок2', self.deck.draw(self.hadsize))
        self.table = Deck()
        self.table.clear()
        self.currentPlayer = self.player1
        self.winner = None

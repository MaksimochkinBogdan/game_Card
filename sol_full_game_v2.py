import random

VALUES = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
SUITS = ('Spades', 'Clubs', 'Diamonds', 'Hearts')
SUITS_UNI = {
    'Spades': '♠',
    'Clubs': '♣',
    'Diamonds': '♦',
    'Hearts': '♥'
}


class Card:
    def __init__(self, value, suit):
        self.value = value  # Значение карты(2, 3... 10, J, Q, K, A)
        self.suit = suit  # Масть карты

    def equal_suit(self, other_card):
        return self.suit == other_card.suit

    def __gt__(self, other_card):
        if self.value == other_card.value:
            return SUITS.index(self.suit) > SUITS.index(other_card.suit)
        return VALUES.index(self.value) > VALUES.index(other_card.value)

    def __lt__(self, other_card):
        if self.value == other_card.value:
            return SUITS.index(self.suit) < SUITS.index(other_card.suit)
        return VALUES.index(self.value) < VALUES.index(other_card.value)

    def __str__(self):
        return self.__repr__()
        # return f"{self.value}{SUITS_UNI[self.suit]}"

    def __repr__(self):
        return f"{self.value}{SUITS_UNI[self.suit]}"


# Задание: Теперь создадим колоду из 52-ух карт и реализуем все методы
class Deck:
    def __init__(self, cards=None):
        # Список карт в колоде. Каждым элементом списка будет объект класса Card
        if cards:
            self.cards = cards
        else:
            self.cards = [Card(v, s) for s in SUITS for v in VALUES]

    def show(self):
        return f"deck[{len(self.cards)}] {','.join([str(card) for card in self.cards])}"

    def __str__(self):
        return f"deck[{len(self.cards)}] {','.join([str(card) for card in self.cards])}"

    def draw(self, x):
        hand = self.cards[:x]
        self.cards = self.cards[x:]
        return hand

    def draw_all(self):
        hand = self.cards[:]
        self.cards = []
        return hand

    def clear(self):
        self.cards = []

    def add(self, cards: [Card]):
        self.cards = self.cards + cards

    def shuffle(self):
        random.shuffle(self.cards)

    def __getitem__(self, index):
        return self.cards[index]


class Player:
    def __init__(self, name, hand: list[Card]):
        self.name = name
        self.hand = hand

    def handsize(self):
        return len(self.hand)

    def make_move(self, table: Deck):

        move_card = None
        if table.cards:
            values_on_table = set([v.value for v in table.cards])
            for v in values_on_table:
                for c in self.hand:
                    if c.value == v:
                        move_card = c
                        break
                if move_card:
                    break
            if not move_card:
                print('Бито.')
                table.clear()
        else:
            if self.hand:
                move_card = min(self.hand)
            else:
                return False

        if move_card:
            print(f'{self.name} | {self.hand}')
            print(f'{self.name} играет {move_card}')
            self.remove_card(move_card)
            table.add([move_card])
            return True
        else:
            return False

    # Если может сходит True если нет False

    def beat_off(self, table: Deck):
        card_to_beat = table.cards[-1]
        print('Побить', card_to_beat)
        cards_for_beat = [c for c in self.hand if c.equal_suit(card_to_beat) and c > card_to_beat]
        print('for beat', cards_for_beat)
        if cards_for_beat:
            card_for_beat = min(cards_for_beat)
        else:
            return False

        print(f'{self.name} отбивает {card_to_beat} - {card_for_beat}')
        self.remove_card(card_for_beat)
        table.add([card_for_beat])
        return True

    def draw(self, deck, number_of_cards):
        self.hand = self.hand + deck.draw(number_of_cards)

    def get_tablecards(self, table: Deck):
        print(f'{self.name} забирает стол.')
        self.hand = self.hand + table.draw_all()
        print(f'{self.name} | {self.hand}')
        print(f'СТОЛ | {table}')
        pass

    def remove_card(self, card: Card):
        self.hand.remove(card)

    def __str__(self):
        return f'{self.name} | {self.hand}'


class Game_machine:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.handsize = 6
        self.player1 = Player('Игрок1', self.deck.draw(self.handsize))
        self.player2 = Player('Игрок2', self.deck.draw(self.handsize))
        self.table = Deck()
        self.table.clear()
        self.currentPlayer = self.player1
        self.winner = None

    def start(self):
        counter = 0
        while not self.game_over():
            counter += 1
            print(f'Раунд {counter}')
            print('_' * 40)
            atacker, blocker = self.choose_roles()

            while atacker.make_move(self.table):
                if blocker.beat_off(self.table):
                    continue
                blocker.get_tablecards(self.table)

            if atacker.handsize() < 6:
                atacker.draw(self.deck, 6 - atacker.handsize())
            if blocker.handsize() < 6:
                blocker.draw(self.deck, 6 - blocker.handsize())

            if atacker.handsize() == 0:
                self.game_over(atacker)
            if blocker.handsize() == 0:
                self.game_over(blocker)

            print('СТОЛ', self.table)
            print('КОЛОДА', self.deck)
            print('====' * 40)
        else:
            print('Победил ' + self.winner)
            print('РАУНД:', counter)
            print('РУКА ИГРОКА1:', self.player1)
            print('РУКА ИГРОКА2:', self.player2)
            print('СТОЛ:', self.deck)
            print('КОЛОДА:', self.deck)

    def game_over(self, player=None):
        if player:
            self.winner = player.name

        if self.winner:
            return True
        return False

    def choose_roles(self):
        if self.currentPlayer == self.player1:
            attacker, blocker = self.player1, self.player2
            self.currentPlayer = self.player2
        else:
            attacker, blocker = self.player2, self.player1
            self.currentPlayer = self.player1

        return attacker, blocker


"""
Cоздадим имитацию ходов в “Дурака без козырей”:

1. Создайте колоду из 52 карт. Перемешайте ее.
2. Первый игрок берет сверху 10 карт
3. Второй игрок берет сверху 10 карт.
4. Игрок-1 ходит:
    4.1. игрок-1 выкладывает самую маленькую карту по "старшенству"
    4.2. игрок-2 пытается бить карту, если у него есть такая же масть, но значением больше.
    4.3. Если игрок-2 не может побить карту, то он проигрывает/забирает себе(см. пункт 7)
    4.4. Если игрок-2 бьет карту, то игрок-1 может подкинуть карту любого значения, которое есть на столе.
5. Если Игрок-2 отбился, то Игрок-1 и Игрок-2 меняются местами. Игрок-2 ходит, Игрок-1 отбивается.
6. Выведите в консоль максимально наглядную визуализацию данных ходов.
7* Реализовать возможность добрать карты из колоды после того, как один из игроков отбился/взял в руку
"""
g = Game_machine()
g.start()

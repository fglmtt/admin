import random


class Card:
    """
    Represent a standard playing card
    """

    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    ranks = [
        None,
        "Ace",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "Ace",
    ]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank_name = Card.ranks[self.rank]
        suit_name = Card.suits[self.suit]
        return f"{rank_name} of {suit_name}"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def to_tuple(self):
        return (self.suit, self.rank)

    def __lt__(self, other):
        # Suit is more important than rank
        # If suits are equal, compare ranks
        return self.to_tuple() < other.to_tuple()

    def __le__(self, other):
        return self.to_tuple() <= other.to_tuple()


class Deck:
    """
    Represent a deck of cards
    """

    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return "\n".join(res)

    def make_cards():
        cards = []
        for suit in range(4):
            # Aces outrank kings
            for rank in range(2, 15):
                card = Card(suit, rank)
                cards.append(card)
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def take_card(self):
        return self.cards.pop()

    def put_card(self, card):
        self.cards.append(card)

    def move_cards(self, other, num):
        for _ in range(num):
            card = self.take_card()
            other.put_card(card)


class Hand(Deck):
    """
    Represent a hand of a player
    """

    def __init__(self, label=""):
        self.label = label
        self.cards = []

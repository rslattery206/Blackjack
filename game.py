import random

deck = []
money = 100


class Card:
    def __init__(self, value_string, suit):
        self.value_string = value_string
        self.suit = suit
        self.id = str(value_string) + str(suit)


def populateDeck():
    deck.append(Card("A", "S"))
    for i in range(2, 11):
        deck.append(Card(i, "S"))
    deck.append(Card("J", "S"))
    deck.append(Card("Q", "S"))
    deck.append(Card("K", "S"))
    deck.append(Card("A", "C"))
    for i in range(2, 11):
        deck.append(Card(i, "C"))
    deck.append(Card("J", "C"))
    deck.append(Card("Q", "C"))
    deck.append(Card("K", "C"))
    deck.append(Card("A", "D"))
    for i in range(2, 11):
        deck.append(Card(i, "D"))
    deck.append(Card("J", "D"))
    deck.append(Card("Q", "D"))
    deck.append(Card("K", "D"))
    deck.append(Card("A", "H"))
    for i in range(2, 11):
        deck.append(Card(i, "H"))
    deck.append(Card("J", "H"))
    deck.append(Card("Q", "H"))
    deck.append(Card("K", "H"))

    for card in deck:
        if type(card.value_string) == str:
            card.val = 10
        else:
            card.val = card.value_string
        if card.value_string == "A":
            card.val = 11


def drawCard():
    return deck.pop(0)


def initializeGame(number_of_decks=6):
    for each_deck in range(0, number_of_decks):
        populateDeck()
    random.shuffle(deck)


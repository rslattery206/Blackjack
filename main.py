import PySimpleGUI as sg

import game

game.initializeGame()
deck = game.deck
money = 100
my_hand = []
dealer_hand = []
my_hand.append(game.drawCard())
dealer_hand.append(game.drawCard())
my_hand.append(game.drawCard())
dealer_hand.append(game.drawCard())


def newRound():
    # Handles the creation of a new round
    my_hand.clear()
    dealer_hand.clear()
    my_hand.append(game.drawCard())
    dealer_hand.append(game.drawCard())
    my_hand.append(game.drawCard())
    dealer_hand.append(game.drawCard())
    # Update Cards
    window["0_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[0].id))
    window["1_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[1].id))
    window["2_PLAYER_CARD"].update(filename="images/blank.png")
    window["3_PLAYER_CARD"].update(filename="images/blank.png")
    window["4_PLAYER_CARD"].update(filename="images/blank.png")
    window["0_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[0].id))
    window["1_DEALER_CARD"].update(filename="images/hidden_card.png")
    # Update Totals
    window["_PLAYER_TOTAL"].update(getTotal(my_hand))
    window["_DEALER_TOTAL"].update(dealer_hand[0].val)
    # Make Buttons Clickable
    window["_PLAYER_DRAW"].update(disabled=False)
    window["_STAND"].update(disabled=False)


def getTotal(hand):
    total = 0
    for card in hand:
        total = total + card.val
    return total


def hit():
    my_hand.append(game.drawCard())
    if (getTotal(my_hand)) > 21:  # bust
        endTurn()


def endTurn():
    # Handles end of player action and performs dealer's actions
    window["_PLAYER_DRAW"].update(disabled=True)
    window["_STAND"].update(disabled=True)
    revealDealerHoleCard()


def revealDealerHoleCard():
    window["1_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[1].id))
    window["_DEALER_TOTAL"].update(getTotal(dealer_hand))


top_bar = [
    sg.Text("$" + str(money)),
    sg.Text("Blackjack 2022", font=("SEC Bengali", 20)),
    sg.Column([[sg.Image(filename="images/icon.png", tooltip="Logo styled using MS Paint")]], justification='right'),
]

dealer_side = [
    [sg.Text("The Dealer")],
    [sg.Text(dealer_hand[0].val, key="_DEALER_TOTAL")],
    [sg.Image(filename="images/{}.png".format(dealer_hand[0].id), key="0_DEALER_CARD"),
     sg.Image(filename="images/hidden_card.png", key="1_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="2_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="3_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="4_DEALER_CARD")]
]

player_side = sg.Column([
    [sg.Text("Player")],
    [sg.Text(getTotal(my_hand), key="_PLAYER_TOTAL")],
    [sg.Image(filename="images/{}.png".format(my_hand[0].id), key="0_PLAYER_CARD"),
     sg.Image(filename="images/{}.png".format(my_hand[1].id), key="1_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="2_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="3_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="4_PLAYER_CARD")]
])

layout = [
    top_bar,
    [dealer_side],
    [player_side],
    # Buttons
    [sg.Button(button_text="Hit", key="_PLAYER_DRAW"),
     sg.Button(button_text="Stand", key="_STAND")],
    [sg.Button(button_text="manual_end_round", key="manual_end_round")]
]

window = sg.Window(title="BlackJack", layout=layout, size=(400, 550))

while True:
    event, values = window.read()
    if event == "_PLAYER_DRAW":
        hit()
        window["_PLAYER_TOTAL"].update(getTotal(my_hand))
        new_card_index = len(my_hand) - 1
        window[str(new_card_index) + "_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[new_card_index].id))
    if event == "_STAND":
        endTurn()
    if event == "manual_end_round":
        newRound()
    elif event == sg.WIN_CLOSED:
        break

window.close()

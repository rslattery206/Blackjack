import PySimpleGUI as sg

import game

game.initializeGame()
deck = game.deck
money = game.money
wager = 0
my_hand = []
dealer_hand = []


def newRound():
    # Handles the creation of a new round
    my_hand.clear()
    dealer_hand.clear()
    my_hand.append(game.drawCard())
    dealer_hand.append(game.drawCard())
    my_hand.append(game.drawCard())
    dealer_hand.append(game.drawCard())
    window["_MONEY"].update("$" + str(game.money))
    # Rare case where player or dealer is dealt 2 aces
    if getTotal(my_hand) == 22:
        my_hand[1].val = 1
    if getTotal(dealer_hand) == 22:
        dealer_hand[1].val = 1
    # Update Cards
    window["0_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[0].id))
    window["1_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[1].id))
    window["2_PLAYER_CARD"].update(filename="images/blank.png")
    window["3_PLAYER_CARD"].update(filename="images/blank.png")
    window["4_PLAYER_CARD"].update(filename="images/blank.png")
    window["0_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[0].id))
    window["1_DEALER_CARD"].update(filename="images/hidden_card.png")
    window["2_DEALER_CARD"].update(filename="images/blank.png")
    window["3_DEALER_CARD"].update(filename="images/blank.png")
    window["4_DEALER_CARD"].update(filename="images/blank.png")
    # Update Totals
    window["_PLAYER_TOTAL"].update(getTotal(my_hand))
    window["_DEALER_TOTAL"].update(dealer_hand[0].val)
    # Configure Buttons
    window["_PLAYER_DRAW"].update(disabled=False)
    window["_STAND"].update(disabled=False)
    window["_NEW_ROUND"].update(disabled=True)
    window["_BET"].update(disabled=True)


def getTotal(hand):
    total = 0
    for card in hand:
        total = total + card.val
    return total


def containsAce(hand):
    i = 0
    for card in hand:
        if card.val == 11:
            return i
        i += 1
    return None


def hit():
    my_hand.append(game.drawCard())
    if (getTotal(my_hand)) > 21:
        if containsAce(my_hand):  # bust
            my_hand[containsAce(my_hand)].val = 1
        else:
            endTurn(True)
    window["_PLAYER_TOTAL"].update(getTotal(my_hand))
    new_card_index = len(my_hand) - 1
    window[str(new_card_index) + "_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[new_card_index].id))


def dealer_hit():
    dealer_hand.append(game.drawCard())
    window["_DEALER_TOTAL"].update(getTotal(dealer_hand))
    new_card_index = len(dealer_hand) - 1
    window[str(new_card_index) + "_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[new_card_index].id))


def endTurn(bust=False):
    window["_PLAYER_DRAW"].update(disabled=True)
    window["_STAND"].update(disabled=True)
    revealDealerHoleCard()
    # Dealer action:
    dealer_bust = False
    if not bust:
        while getTotal(dealer_hand) < 17 or (getTotal(dealer_hand) == 17 and containsAce(dealer_hand)):
            dealer_hit()
            dealer_bust = (getTotal(dealer_hand) > 21)
            if dealer_bust and containsAce(dealer_hand):
                dealer_bust = False
                dealer_hand[containsAce(dealer_hand)].val = 1
            if getTotal(dealer_hand) == 17 and containsAce(dealer_hand):
                dealer_hit()

    new_money = 0
    if len(my_hand) == 2 and getTotal(my_hand) == 21:  # Blackjack
        new_money = game.money + 1.5 * wager
    elif bust:  # Player busted and lost
        new_money = game.money - wager
    elif not bust and dealer_bust:
        new_money = game.money + wager
    elif getTotal(dealer_hand) < getTotal(my_hand):
        new_money = game.money + wager
    elif getTotal(dealer_hand) > getTotal(my_hand):
        new_money = game.money - wager
    elif getTotal(dealer_hand) == getTotal(my_hand):
        new_money = game.money
    game.money = new_money
    window["_MONEY"].update("$" + str(game.money))
    window["_NEW_ROUND"].update(disabled=False)


def revealDealerHoleCard():
    window["1_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[1].id))
    window["_DEALER_TOTAL"].update(getTotal(dealer_hand))


top_bar = [
    sg.Text("$" + str(money), key="_MONEY"),
    sg.Text("Blackjack 2022", font=("SEC Bengali", 20)),
    sg.Column([[sg.Image(filename="images/icon.png", tooltip="Logo styled using MS Paint")]], justification='right'),
]

dealer_side = [
    [sg.Text("The Dealer")],
    [sg.Text(key="_DEALER_TOTAL")],
    [sg.Image(filename="images/blank.png", key="0_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="1_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="2_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="3_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="4_DEALER_CARD")]
]

player_side = sg.Column([
    [sg.Text("Player")],
    [sg.Text(getTotal(my_hand), key="_PLAYER_TOTAL")],
    [sg.Image(filename="images/blank.png", key="0_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="1_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="2_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="3_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="4_PLAYER_CARD")]
])

layout = [
    top_bar,
    [dealer_side],
    [player_side],
    # Buttons
    [sg.Button(button_text="Hit", key="_PLAYER_DRAW", disabled=True),
     sg.Button(button_text="Stand", key="_STAND", disabled=True)],
    # Betting
    [sg.In(5, key="_BET", size=(10, 1)), sg.Button(button_text="Place Bet and Deal", key="_NEW_ROUND")],

]

window = sg.Window(title="BlackJack", layout=layout, size=(400, 550))
while True:
    event, values = window.read()
    if event == "_PLAYER_DRAW":
        hit()
    if event == "_STAND":
        endTurn(False)
    if event == "_NEW_ROUND":
        newRound()
        wager = int(values["_BET"])
    elif event == sg.WIN_CLOSED:
        break

window.close()

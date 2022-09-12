import math

import PySimpleGUI as sg
from time import sleep
import game

game.initializeGame()
deck = game.deck
wager = 5
my_hand = []
dealer_hand = []
sleep_time = 0.5


#  TODO List:
#  Dealer Blackjack
#  Insurance
#  Double Down
#
# TODO List (Further down the road):
# Settings (change colors, theme, set money, misc. preferences)
# Logging (keeps tracks of all data)


def newRound():
    # Handles the creation of a new round
    my_hand.clear()
    dealer_hand.clear()

    # For hard-coding cards:
    # card1 = game.Card(value_string="A", suit="S")
    # card2 = game.Card(value_string="9", suit="S")
    # card1.val = 11
    # card2.val = 9
    # my_hand.append(card1)
    # my_hand.append(card2)

    my_hand.append(game.drawCard())
    my_hand.append(game.drawCard())
    dealer_hand.append(game.drawCard())
    dealer_hand.append(game.drawCard())
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
    window["5_PLAYER_CARD"].update(filename="images/blank.png")
    window["0_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[0].id))
    window["1_DEALER_CARD"].update(filename="images/hidden_card.png")
    window["2_DEALER_CARD"].update(filename="images/blank.png")
    window["3_DEALER_CARD"].update(filename="images/blank.png")
    window["4_DEALER_CARD"].update(filename="images/blank.png")
    window["5_DEALER_CARD"].update(filename="images/blank.png")
    # Update Totals
    window["_PLAYER_TOTAL"].update(getTotal(my_hand))
    window["_DEALER_TOTAL"].update(dealer_hand[0].val)
    # Configure Buttons
    window["_PLAYER_DRAW"].update(disabled=False)
    window["_STAND"].update(disabled=False)
    if (wager * 2) <= game.money:
        window["_DOUBLE"].update(disabled=False)
    window["_NEW_ROUND"].update(disabled=True)
    window["+5"].update(disabled=True)
    window["-5"].update(disabled=True)


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
        if containsAce(my_hand) is not None:
            my_hand[containsAce(my_hand)].val = 1
        else:
            endTurn(True)
    window["_PLAYER_TOTAL"].update(getTotal(my_hand))
    new_card_index = len(my_hand) - 1
    window[str(new_card_index) + "_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[new_card_index].id))
    window["_DOUBLE"].update(disabled=True)


def dealer_hit():
    dealer_hand.append(game.drawCard())
    window["_DEALER_TOTAL"].update(getTotal(dealer_hand))
    new_card_index = len(dealer_hand) - 1
    window[str(new_card_index) + "_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[new_card_index].id))


def go_broke():
    # Function for force-quitting the game (e.g when the player runs out of money)
    no_money_window = sg.Window(title="You're broke", layout=[[sg.Text("Looks like you've gone broke. Goodbye!")]])
    while True:
        event2, values2 = no_money_window.read()
        if event2 == sg.WIN_CLOSED:
            window.close()
            break


def endTurn(bust=False):
    window["_PLAYER_DRAW"].update(disabled=True)
    window["_STAND"].update(disabled=True)
    window["_DOUBLE"].update(disabled=True)
    revealDealerHoleCard()
    new_money = 0
    if len(my_hand) == 2 and getTotal(my_hand) == 21:  # Blackjack
        new_money = game.money + 1.5 * wager
    else:
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

        if bust:  # Player busted and lost
            new_money = game.money - wager
            window["_MAIN"].update("You lose.")
        elif not bust and dealer_bust:
            new_money = game.money + wager
            window["_MAIN"].update("You win!")
        elif getTotal(dealer_hand) < getTotal(my_hand):
            window["_MAIN"].update("You win!")
            new_money = game.money + wager
        elif getTotal(dealer_hand) > getTotal(my_hand):
            new_money = game.money - wager
            window["_MAIN"].update("You lose.")
        elif getTotal(dealer_hand) == getTotal(my_hand):
            new_money = game.money
            window["_MAIN"].update("Push.")
    game.money = new_money
    window["_MONEY"].update("$" + str(game.money))
    window["_NEW_ROUND"].update(disabled=False)
    window["-5"].update(disabled=False)
    window["+5"].update(disabled=False)
    if (wager + 5) > game.money:
        window["+5"].update(disabled=True)
    if (wager - 5) < 5:
        window["-5"].update(disabled=True)
    if game.money < 5:
        window["_MAIN"].update("$5 minimum bet :(")
        go_broke()


def revealDealerHoleCard():
    window["1_DEALER_CARD"].update(filename="images/{}.png".format(dealer_hand[1].id))
    window["_DEALER_TOTAL"].update(getTotal(dealer_hand))


top_bar = [
    sg.Text("Blackjack 2022", font=("Times New Roman", 20, "bold")),
    sg.Column([[sg.Image(filename="images/icon.png", tooltip="Logo styled using MS Paint")]], justification='right'),
]

dealer_side = [
    [sg.Text("The Dealer")],
    [sg.Text(key="_DEALER_TOTAL")],
    [sg.Image(filename="images/blank.png", key="0_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="1_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="2_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="3_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="4_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="5_DEALER_CARD")]
]

player_side = sg.Column([
    [sg.Text("Player")],
    [sg.Text(getTotal(my_hand), key="_PLAYER_TOTAL")],
    [sg.Image(filename="images/blank.png", key="0_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="1_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="2_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="3_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="4_PLAYER_CARD"),
     sg.Image(filename="images/blank.png", key="5_PLAYER_CARD")]
])

action_buttons = [sg.Button(button_text="Hit", key="_PLAYER_DRAW", disabled=True),
                  sg.Button(button_text="Stand", key="_STAND", disabled=True),
                  sg.Button(button_text="Double", key="_DOUBLE", disabled=True),
                  ]

layout = [
    top_bar,
    [dealer_side],
    [player_side],
    # Buttons
    action_buttons,
    # Betting
    [
        [sg.Button("-5", key="-5", size=(2, 1), disabled=True),
         sg.Button("+5", key="+5", size=(2, 1))],
        [sg.Text("$" + str(game.money), key="_MONEY", font=("SEC Bengali", 20), text_color="lime"),
         sg.In(5, key="_BET", size=(4, 1), disabled=True),
         sg.Button(button_text="Place Bet and Deal", key="_NEW_ROUND"),
         sg.Text("Place your bet", font=("Times New Roman", 20), key="_MAIN")]
    ],

]

window = sg.Window(title="BlackJack", layout=layout, size=(470, 550))
while True:
    event, values = window.read()
    if event == "_PLAYER_DRAW":
        hit()
        sleep(sleep_time)
        if wager > game.money:
            wager = math.floor(game.money)
            window["+5"].update(disabled=True)
            window["_BET"].update(wager)

    if event == "_DOUBLE":
        sleep(sleep_time)
        wager = wager * 2
        window["_BET"].update(wager)
        hit()
        if getTotal(my_hand) < 21:
            endTurn(bust=False)
        if wager > game.money:
            wager = math.floor(game.money)
            window["+5"].update(disabled=True)
            window["_BET"].update(wager)

    if event == "_STAND":
        sleep(sleep_time)
        endTurn(bust=False)
        if wager > game.money:
            wager = math.floor(game.money)
            window["+5"].update(disabled=True)
            window["_BET"].update(wager)

    if event == "_NEW_ROUND":
        sleep(sleep_time)
        wager = int(values["_BET"])
        newRound()
        window["_MAIN"].update("Your action.")
        if getTotal(my_hand) == 21:
            endTurn(bust=False)

    if event == "+5":
        wager += 5
        window["_BET"].update(wager)
        if (wager + 5) > game.money:
            window["+5"].update(disabled=True)
        window["-5"].update(disabled=False)

    if event == "-5":
        wager -= 5
        window["_BET"].update(wager)
        if (wager - 5) < 5:
            window["-5"].update(disabled=True)
        window["+5"].update(disabled=False)

    elif event == sg.WIN_CLOSED:
        break

window.close()

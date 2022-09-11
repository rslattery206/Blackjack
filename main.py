import PySimpleGUI as sg

import game

game.initializeGame()
deck = game.deck

my_hand = []
dealer_hand = []
my_hand.append(game.drawCard())
dealer_hand.append(game.drawCard())
my_hand.append(game.drawCard())
dealer_hand.append(game.drawCard())


def getTotal(hand):
    total = 0
    for card in hand:
        total = total + card.val
    return total


top_bar = [
    sg.Text("Blackjack 2022", font=("SEC Bengali", 20)),
    sg.Column([[sg.Image(filename="images/icon.png", tooltip="Logo styled using MS Paint")]], justification='right')
]

dealer_side = [
    [sg.Text("The Dealer")],
    [sg.Text(getTotal(dealer_hand))],
    [sg.Image(filename="images/{}.png".format(dealer_hand[0].id), key="0_DEALER_CARD"),
     sg.Image(filename="images/hidden_card.png", key="1_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="2_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="3_DEALER_CARD"),
     sg.Image(filename="images/blank.png", key="4_DEALER_CARD")]
]
#    [sg.Image(filename="images/{}.png".format(card.id), key='420') for card in my_hand]

player_side = sg.Column([
    [sg.Text("Player")],
    [sg.Text(getTotal(my_hand), key="PLAYER_TOTAL")],
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
    [sg.Button(button_text="Add Card", key="_HIT")],
]

window = sg.Window(title="durrr", layout=layout, size=(400, 500))
while True:
    event, values = window.read()
    if event == "_HIT":
        #HIT
        my_hand.append(game.drawCard())
        window["PLAYER_TOTAL"].update(getTotal(my_hand))
        new_card_index = len(my_hand) - 1
        window[str(new_card_index) + "_PLAYER_CARD"].update(filename="images/{}.png".format(my_hand[new_card_index].id))
    elif event == sg.WIN_CLOSED:
        break

window.close()

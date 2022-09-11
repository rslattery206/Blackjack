import PySimpleGUI as sg

layout = [
    [sg.Text("Whats up everybody")],
    [sg.Button("urh"), sg.Image(filename='123.png', size=(150,150))],
    [sg.Button('dook')]
]

window = sg.Window(title = "Durrr", layout=layout)

while True:
    event, values = window.read()
    if event == "dook" or event == sg.WIN_CLOSED:
        break

window.close()

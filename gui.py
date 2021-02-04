import PySimpleGUI as sg

sg.theme("DarkTeal11")
layout = [[sg.T("")], [sg.Text("Datei: "), sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-IN-")],[sg.Button("Parse") , sg.Button("Exit")]]

###Building Window
window = sg.Window('Etherpad-Parser', layout, size=(600,150))
    
while True:
    event, values = window.read()
    print(values["-IN2-"])
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Parse":
        print(values["-IN-"])
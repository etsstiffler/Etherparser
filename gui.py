import PySimpleGUI as sg

sg.theme("DarkTeal11")
layout = [[sg.T("")], [sg.Text("Datei: "), sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-INPUTFILE-", file_types=(("Etherpad Files", "*.etherpad"),))],[sg.Button("OK") , sg.Button("Exit")]]

###Building Window
window = sg.Window('Etherpad-Parser', layout, size=(600,150))
    
while True:
    event, values = window.read()
    print(values["-IN2-"])
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "OK":
        file = values["-INPUTFILE-"]
        try:
            file.endswith('.etherpad')
            print(file)
        except:
            sg.Popup('Error', 'Falsches Dateiformat')
        

        

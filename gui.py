import PySimpleGUI as sg
import pandas as pd
from datetime import datetime

sg.theme("DarkTeal11")
def make_win1():
    layout = [[sg.Text("Datei: "), sg.Input(key="-INPUTFILE-" ,change_submits=True),sg.FileBrowse(key="-IN-", file_types=(("Etherpad Files", "*.etherpad"),))],
    [sg.Button("OK") , sg.Button("Exit")]]
    return sg.Window('Etherpad-Parser', layout, location=(800,600), finalize=True)


def make_win2():
    layout = [[sg.Text('The second window')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25,1), k='-OUTPUT-')],
              [sg.Button('Erase'), sg.Button('Popup'), sg.Button('Exit')]]
    return sg.Window('Etherpad-Parser', layout, finalize=True)


###Building Window
window1, window2 = make_win1(), None        # start off with 1 window open
    
while True:
    window, event, values = sg.read_all_windows()
    #print(values["-IN2-"])
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    elif event == "OK" and not window2:
        try:
            file = values["-INPUTFILE-"]
            print(file)
            try:
                data = pd.read_json(file)
                window2 = make_win2()
            #     data = pd.read_json(args.file)


            #     #extract relevant Data frpm DF time, author, chars --> history
            #     authors = {}
            #     history = list()

            #     # Iterate over the sequence of column names save Authors
            #     for column in data:
            #         columnSeriesObj = data[column]
            #         # Check global Authors
            #         if 'globalAuthor' in column:
            #                 # Pseudonyme der Autoren auslesen
            #                 cipher = column.split(":")[1]
            #                 # Realer Name
            #                 name = columnSeriesObj.values[8]
            #                 authors[cipher]= name

            #     # Iterate over the sequence of column names 
            #     for column in data:
            #         columnSeriesObj = data[column]    
            #         if 'pad' in column:
            #             tmp = str(columnSeriesObj.values[12])
            #         try:
                        
            #             tmp = eval(tmp)
            #             author = tmp['author']
            #             timestamp = int(tmp['timestamp']) / 1000.0
            #             time = datetime.fromtimestamp(timestamp)
            #             time = time.strftime("%d %b %Y %H:%M:%S")
                    
            #             realauthor=authors[author]
            #             changes = str(columnSeriesObj.values[11])
            #             changes = changes.split("$")
            #             changes = changes[1]
            #             if changes == '':
            #                 changes = "DELETE"
            #             history.append([time,realauthor,changes])
            #         except: pass
            except:
                sg.Popup('Fehler','Keine Datei ausgewählt')
        except:
            sg.Popup('Error', 'Something went wrong')
        

        

import PySimpleGUI as sg
import pandas as pd
from datetime import datetime

sg.theme("DarkTeal11")

def make_win1():
    layout = [[sg.Text("Datei: "),sg.Input(key="-INPUTFILE-" , change_submits=True),sg.FileBrowse(key="-IN-", file_types=(("Etherpad Files", "*.etherpad"),),initial_folder='')],
    [sg.Text('Verlauf:',visible=False, key="-txt-")],
    [sg.Multiline(key='-out-', size=(80, 20), visible=False, font='ANY 11')],
    [place(sg.Button("Parse",key="-parse-", visible=True)) , place(sg.InputText(key='Save as', do_not_clear=False, enable_events=True, visible=False)),
    place(sg.FileSaveAs(initial_folder='',file_types=(('Text', '.txt'), ('CSV', '.csv')))) , place(sg.Button("Exit"))]]
    return sg.Window('Etherpad-Parser', layout, location=(100,100), finalize=True)


def parse(file):
    data = pd.read_json(file)

    #extract relevant Data frpm DF time, author, chars --> history
    authors = {}
    history = list()

    # Iterate over the sequence of column names save Authors
    for column in data:
        columnSeriesObj = data[column]
        # Check global Authors
        if 'globalAuthor' in column:
            # Pseudonyme der Autoren auslesen
            cipher = column.split(":")[1]
            # Realer Name
            name = columnSeriesObj.values[8]
            authors[cipher]= name

            # Iterate over the sequence of column names 
            for column in data:
                columnSeriesObj = data[column]    
                if 'pad' in column:
                    tmp = str(columnSeriesObj.values[12])
                try:   
                    tmp = eval(tmp)
                    author = tmp['author']
                    timestamp = int(tmp['timestamp']) / 1000.0
                    time = datetime.fromtimestamp(timestamp)
                    time = time.strftime("%d %b %Y %H:%M:%S")
                    
                    realauthor=authors[author]
                    input = str(columnSeriesObj.values[11])
                    input = input.split("$")
                    input = input[1]
                    if input == '':
                        input = "DELETE"
                    history.append([time,realauthor,input])
                except: pass

    return history

def place(elem):
    '''
    Places element provided into a Column element so that its placement in the layout is retained.
    :param elem: the element to put into the layout
    :return: A column element containing the provided element
    '''
    return sg.Column([[elem]], pad=(0,0))


###Building Window
window = make_win1()   


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "-parse-":
        try:

            file = values["-INPUTFILE-"]
            try:
                notes = parse(file)
                window.FindElement('-out-').Update(visible=True)
                window.FindElement('-txt-').Update(visible=True)
                window.Element('-out-').Update('')
                try:
                    for item in notes:
                        string = "%s %s %s \n"%(item[0],item[1],item[2])
                        window.Element('-out-').Update(string, append=True)
                except:
                    print(string)
            except:
                sg.Popup('Fehler','Keine Datei ausgewählt')
        except:pass
    # elif event == "Save as":
    #     try:
            
    #     except:
    #         sg.Popup('Fehler','Bitte erst Datei parsen')



        

        

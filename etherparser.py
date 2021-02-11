#  Copyright 2021 fdre 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import sys
import PySimpleGUI as sg
import json
from datetime import datetime
import os

sg.theme("DarkTeal11")

## fix missing icon after building with pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def place(elem):
    '''
    Places element provided into a Column element so that its placement in the layout is retained.
    :param elem: the element to put into the layout
    :return: A column element containing the provided element
    '''
    return sg.Column([[elem]], pad=(0,0))


def make_win1():
    layout = [[sg.Text("Datei: "),sg.Input(key="-INPUTFILE-" ,enable_events=True, change_submits=True),sg.FileBrowse(key="-IN-", target="-INPUTFILE-", file_types=(("Etherpad Files", "*.etherpad"),),initial_folder='')],
    [sg.Text('Verlauf:',visible=False, key="-txt-")],
    [sg.Multiline(key='-out-', size=(80, 20), visible=False)],
    [place(sg.InputText(key='-save-', do_not_clear=False, enable_events=True, visible=False)),
    place(sg.FileSaveAs(target="-save-", initial_folder='',file_types=(('Text', '.txt'), ('CSV', '.csv')))) , place(sg.Button("Exit"))]]
    return sg.Window('Etherpadparser', layout, icon=resource_path("logo.ico"), location=(100,100), finalize=True)


def parse(file):
    file = open(file,"r")
    data = json.load(file)

    #extract relevant Data time, author, text --> history
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
            name = columnSeriesObj['name']
            authors[cipher]= name

    # Iterate over the sequence of column names
    for column in data:
        columnSeriesObj = data[column]   
        if 'pad' in column:
            try:
                author = columnSeriesObj['meta']['author']
                timestamp = int(columnSeriesObj['meta']['timestamp']) / 1000.0
                time = datetime.fromtimestamp(timestamp)
                time = time.strftime("%d %b %Y %H:%M:%S")

                realauthor=authors[author]
                input = columnSeriesObj['changeset']

                input = input.split("$")
                input = input[1]
                if input == '':
                    input = "DELETE"
                history.append([time,realauthor,input])
            except: pass

    return history



###Building Window
window = make_win1()   


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "-INPUTFILE-" or event=="-parse-":
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
                    sg.Popup('Fehler','Es gab einen Fehler bitte Entickler kontaktieren')
            except:
                sg.Popup('Fehler','Keine Datei ausgewählt')
        except:pass
    elif event == "-save-":
        try:
            
            filename = values["-save-"]
            f = open(filename,"w")
            f.write(values["-out-"])
            f.close()
            os.startfile(filename)
        except:
            sg.Popup('Fehler','Task failed successfull')




        

        

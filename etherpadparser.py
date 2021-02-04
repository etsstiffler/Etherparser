import argparse
import os.path
import json
import pandas as pd
from datetime import datetime
import PySimpleGUI as sg

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        if arg.endswith('.json'):
            return open(arg, 'r') 
        elif arg.endswith('.etherpad'):
            return open(arg, 'r')
        else:
            parser.error("The file %s is not a JSON or Ehterpad file." % arg)


#parsing Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="file", required=True,
                    help="input file to parse", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()


data = pd.read_json(args.file)


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
        changes = str(columnSeriesObj.values[11])
        changes = changes.split("$")
        changes = changes[1]
        if changes == '':
            changes = "DELETE"
        history.append([time,realauthor,changes])
    except: pass

#Ausgabe erstellen

if not os.path.exists('chat.csv'):
    with open("chat.csv", "a") as myfile:
        for item in history:
            myfile.write("%s %s %s \n"%(item[0],item[1],item[2]))
else:
    with open("chat.csv", "w") as myfile:
        for item in history:
            myfile.write("%s %s %s \n"%(item[0],item[1],item[2]))



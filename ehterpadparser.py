import argparse
import json
import pandas as pd
from datetime import datetime

#parsing Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", help="file to parse")
args = parser.parse_args()

file = args.f

data = pd.read_json(file)

authors = {}
notes = list()

# Iterate over the sequence of column names
for column in data:
   columnSeriesObj = data[column]
   # Check global Authors
   if 'globalAuthor' in column:
        # Pseudonyme der Autoren auslesen
        cipher = column.split(":")[1]
        # Realer Name
        name = columnSeriesObj.values[8]
        authors[cipher]= name

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
        notes.append(changes[1])

        #print("author is {author} at {timestamp}".format(**tmp))
    except: pass

str1 = ''.join(str(e) for e in notes)
print(str1)
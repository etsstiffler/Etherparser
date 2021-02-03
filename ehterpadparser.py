import argparse
import json
import pandas as pd

#parsing Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", help="file to parse")
args = parser.parse_args()

file = args.f

data = pd.read_json(file)

authors = list()
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
        authors.append([cipher,name])

for column in data:
    columnSeriesObj = data[column]    
    if 'pad' in column:
        tmp = str(columnSeriesObj.values[12])
        tmp2 = len(tmp.split("'"))
        print(tmp2)
        #notes.append([authors[columnSeriesObj.values[12][1]])
        # print('Colunm Name : ', column)
        # print('Column Contents : ', columnSeriesObj.values)
#print(authors)
    
#print(authors)
# for col in data.columns: 
#     print(col) 


# spike_cols = [col for col in data.columns if 'globalAuthor' in col]
# print(list(data.columns))
# print(spike_cols)
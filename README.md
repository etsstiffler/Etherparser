# Etherpadparser 

This tool allows to view chronological changes in a BBB Ehterpad known as "Geteilte Notizen"

## Requirements
* Python >=3.8.5
* Tkinter

Ubuntu:
```
sudo apt install python3-tk

```

## Installation
``` 
git clone 

pip install -r requirements.txt
```

## Usage
Notice: You need an *.etherpad*-file from BBB. Hit "Geteilte Notizen->Export", choose *Etherpad* an save the file.
Commandline:
```
python cli-etherparser.py -f /path/to/etherpadfile
``` 
This will read the etherpadfile and saves the output to *chat.csv* in the same directory

Using the GUI
- Windows: Use the latest .exe file from releases.
- Linux:
```
python etherparser.py
```

Building EXE-File (requires pyinstaller on Windows)

```
pyinstaller -wF -i 'logo.ico' --clean --add-data="logo.ico;." .\etherparser.py
```
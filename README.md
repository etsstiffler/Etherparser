# Etherpadparser 

This tool allows to view chronological changes in a BBB Etherpad known as "Geteilte Notizen"

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

### Commandline:
```
python cli-etherparser.py /path/to/etherpadfile
``` 
This will read the etherpad file and saves the output to `<etherpadfile>.log` in the same directory.

There are more options you can use:
```
usage: cli-etherparser.py [-h] [-l] [-c] [-u] [-a] [--sep SEPARATOR]
                          [-o OUTPUT_DIR]
                          file [file ...]

Convert one ore more etherpad files into a readable format.

positional arguments:
  file               the etherpad files to parse

optional arguments:
  -h, --help         show this help message and exit
  -l, --log          export the etherpad content in a log like format
  -c, --csv          export the etherpad content in a csv format
  -u, --author-list  export the etherpad content as a list of the authors
                     along with their contributions
  -a, --all          export the etherpad content in all formats
  --sep SEPARATOR    the separator used for CSV files
  -o OUTPUT_DIR      the output directory

```

### Using the GUI
- Windows: Use the latest .exe file from releases.
- Linux:
```
python etherparser.py
```

### Building EXE-File (requires pyinstaller on Windows)

```
pyinstaller -wF -i 'logo.ico' --clean --add-data="logo.ico;." .\etherparser.py
```
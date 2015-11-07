# pi-scanner
Barcode scanner project for the Raspberry Pi.

# Table of Contents
* **[Requirements](#requirements)**
* **[Installation](#installation)**
* **[Running](#running)**

_Notes:_

1. _These instructions are for Debian based systems._
2. _These instructions should be performed on the system which will be running the program._

## Requirements
* git
```
sudo apt-get install git
```
* python2.7
```
sudo apt-get install python2.7
```
* python-pip
```
sudo apt-get install python-pip
```
* [gspread](https://github.com/burnash/gspread)
 * Follow the instructions on how to create an oauth [key and file](http://gspread.readthedocs.org/en/latest/oauth2.html)

## Installation
* Use git to clone the project
```
git clone https://github.com/DWiechert/pi-scanner.git
```
* Download the oauth file created in the [requirements](#requirements)

## Running
To run, 3 command line arguments are required:
* `-i` - OAuth file - this is the oauth file downloaded in the [requirements](#requirements) section
* `-sn` - The name of the excel sheet.
* `-ws` - The name of the work sheet

An example run is:
```
python pi-scanner.py -i <path to oauth json file> -sn <excel spreadsheet name> -ws <worksheet name>

dan@cbpp:~/documents/pi-scanner$ python pi-scanner.py -i oauth.json -sn "My Excel Spreadsheet" -ws "Sheet1"

========================================
Input file is [oauth.json].
Excel sheet name is [My Excel Spreadsheet].
Work sheet name is [Sheet1].
========================================
```
The `-h` option is available to see the options:
```
dan@cbpp:~/documents/pi-scanner$ python pi-scanner.py -h
usage: pi-scanner.py [-h] -i OAUTHFILE -sn SHEETNAME -ws WORKSHEET

pi-scanner - Barcode scanner project for the Raspberry Pi.

optional arguments:
  -h, --help     show this help message and exit
  -i OAUTHFILE   OAuth file.
  -sn SHEETNAME  The name of the excel sheet.
  -ws WORKSHEET  The name of the work sheet.
dan@cbpp:~/documents/pi-scanner$ 
```

Once running, just enter in the barcode you would like to search for:
```
Enter the barcode: <input>
Barcode is <input>
```
If the barcode is found, it will print out the row and column:
```
Enter the barcode: asdf
Barcode is asdf

Barcode found at row 13 column 1
```
If the barcode is not found, it will insert the barcode as a new cell:
```
Enter the barcode: asdf
Barcode is asdf

Barcode added at row 13 column 1
```
To quit, just enter `quit` as the barcode:
```
Enter the barcode: quit
dan@cbpp:~/documents/piscanner$
```

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
The `-h` option is available to see the options:
```
dan@cbpp:~/documents/pi-scanner$ python pi-scanner.py -h
usage: pi-scanner.py [-h] -i OAUTHFILE -sn SHEETNAME -ws WORKSHEET
                     [-sfr SEARCHFILTERROW | -sfc SEARCHFILTERCOL]
                     [-vfr VALUEFILTERROW | -vfc VALUEFILTERCOL]

pi-scanner - Barcode scanner project for the Raspberry Pi.

optional arguments:
  -h, --help            show this help message and exit
  -i OAUTHFILE          OAuth file.
  -sn SHEETNAME         The name of the excel sheet.
  -ws WORKSHEET         The name of the work sheet.
  -sfr SEARCHFILTERROW  Row number for search filtering results.
  -sfc SEARCHFILTERCOL  Column number for search filtering results.
  -vfr VALUEFILTERROW   Row number for value filtering results.
  -vfc VALUEFILTERCOL   Column number for value filtering results.
dan@cbpp:~/documents/pi-scanner$
```
To run, the following 3 command line arguments are required:
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

To specify certain columns to query barcodes and values by, use the additional command line options:
```
dan@cbpp:~/documents/pi-scanner$ python pi-scanner.py -i /home/dan/downloads/Pi-Scanner-0cfdd60eae49.json -ws Sheet1 -sn "Test Sheet 1" -sfc 1 -vfc 3

========================================
Input file is [/home/dan/downloads/Pi-Scanner-0cfdd60eae49.json].
Excel sheet name is [Test Sheet 1].
Work sheet name is [Sheet1].
Search filtering on column [1].
Value filtering on column [3].
========================================
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
Enter the barcode: 82050004696506142016
Barcode is [82050004696506142016].
Barcode found at row [17] column [1].
Value found is [456].

Enter the barcode: 261690866007991418
Barcode is [261690866007991418].
Barcode found at row [16] column [1].
Value found is [123].

Enter the barcode: quit
dan@cbpp:~/documents/pi-scanner$
```

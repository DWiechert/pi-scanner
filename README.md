# pi-scanner
Barcode scanner project for the Raspberry Pi.

# Table of Contents
* **[Requirements](#requirements)**
* **[Installation](#installation)**
* **[Running](#running)**

## Requirement

## Installation

## Running
To run, the oauth file downloaded in the [requirements](#requirements) must be passed in with the `-i` argument:
```
python pi-scanner.py -i <path to oauth json file>
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

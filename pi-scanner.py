"""
pi-scanner
Barcode scanner project for the Raspberry Pi.
"""

import sys, argparse
import json
import gspread
from gspread.exceptions import CellNotFound
from oauth2client.client import SignedJwtAssertionCredentials

def _check_negative(value):
    ivalue = int(value)
    if ivalue < 1:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def _filterByRow(seq, row):
	for element in seq:
		if element.row == row:
			return element
	raise CellNotFound

def _filterByCol(seq, col):
	for element in seq:
		if element.col == col:
			return element
	raise CellNotFound

def main():
	# Parse the command line arguments - https://docs.python.org/2/library/argparse.html
	parser = argparse.ArgumentParser(description='pi-scanner - Barcode scanner project for the Raspberry Pi.', prefix_chars='-')
	parser.add_argument('-i', dest='oauthFile', action='store', required=True, help='OAuth file.')
	parser.add_argument('-sn', dest='sheetName', action='store', required=True, help='The name of the excel sheet.')
	parser.add_argument('-ws', dest='worksheet', action='store', required=True, help='The name of the work sheet.')
	search_group = parser.add_mutually_exclusive_group()
	search_group.add_argument('-rf', dest='rowFilter', action='store', help='Row number to filter results by.', type=_check_negative)
	search_group.add_argument('-cf', dest='colFilter', action='store', help='Column number to filter results by.', type=_check_negative)

	args = parser.parse_args()

	oauthFile = args.oauthFile
	sheetName = args.sheetName
	worksheet = args.worksheet
	rowFilter = args.rowFilter
	colFilter = args.colFilter

	print('\n========================================')
	print('Input file is [%s].' % oauthFile)
	print('Excel sheet name is [%s].' % sheetName)
	print('Work sheet name is [%s].' % worksheet)
	if rowFilter is not None:
		print ('Filtering on row [%s].' % rowFilter)
	if colFilter is not None:
		print ('Filtering on column [%s].' % colFilter)
	print('========================================\n')

	# Login through oauth (#6) - http://gspread.readthedocs.org/en/latest/oauth2.html
	json_key = json.load(open(oauthFile))
	scope = ['https://spreadsheets.google.com/feeds']

	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

	# Open the specified excel sheet and worksheet - http://gspread.readthedocs.org/en/latest/index.html
	gc = gspread.authorize(credentials)
	wks = gc.open(sheetName).worksheet(worksheet)

	print('Cell A1 is [%s].' % wks.acell('A1').value)
	print('Cell A2 is [%s].' % wks.acell('A2').value)
	print('Cell B1 is [%s].' % wks.acell('B1').value)
	print('Cell B2 is [%s].' % wks.acell('B2').value)

	while True:    # Read input forever
		barcode = raw_input("\nEnter the barcode: ")
		if barcode == "quit":
			break  # Exit the program

		print('Barcode is [%s].' % barcode)
		try:
			if rowFilter is not None:
				cell = _filterByRow(wks.findall(barcode), rowFilter)
			elif colFilter is not None:
				cell = _filterByCol(wks.findall(barcode), colFilter)
			else:
				cell = wks.find(barcode)
			print('Barcode found at row [%s] column [%s].' % (cell.row, cell.col))
		except CellNotFound:
			wks.add_rows(1)
			row_count = wks.row_count
			wks.update_cell(row_count, 1, barcode)
			cell = wks.find(barcode)
			print('Barcode added at row [%s] column [%s].' % (cell.row, cell.col))

if __name__ == "__main__":
    main()

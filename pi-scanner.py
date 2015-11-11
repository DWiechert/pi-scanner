"""
pi-scanner
Barcode scanner project for the Raspberry Pi.
"""

import sys, argparse
import json
import gspread
from gspread.exceptions import CellNotFound
from oauth2client.client import SignedJwtAssertionCredentials

def _check_positive(value):
    ivalue = int(value)
    if ivalue < 1:
         raise argparse.ArgumentTypeError("[%s] must be a positive integer." % value)
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
	search_group.add_argument('-sfr', dest='searchFilterRow', action='store', help='Row number for search filtering results.', type=_check_positive)
	search_group.add_argument('-sfc', dest='searchFilterCol', action='store', help='Column number for search filtering results.', type=_check_positive)
	value_group = parser.add_mutually_exclusive_group()
	value_group.add_argument('-vfr', dest='valueFilterRow', action='store', help='Row number for value filtering results.', type=_check_positive)
	value_group.add_argument('-vfc', dest='valueFilterCol', action='store', help='Column number for value filtering results.', type=_check_positive)

	args = parser.parse_args()

	oauthFile = args.oauthFile
	sheetName = args.sheetName
	worksheet = args.worksheet
	searchFilterRow = args.searchFilterRow
	searchFilterCol = args.searchFilterCol
	valueFilterRow = args.valueFilterRow
	valueFilterCol = args.valueFilterCol

	print('\n========================================')
	print('Input file is [%s].' % oauthFile)
	print('Excel sheet name is [%s].' % sheetName)
	print('Work sheet name is [%s].' % worksheet)
	if searchFilterRow is not None:
		print ('Search filtering on row [%s].' % searchFilterRow)
	if searchFilterCol is not None:
		print ('Search filtering on column [%s].' % searchFilterCol)
	if valueFilterRow is not None:
		print ('Value filtering on row [%s].' % valueFilterRow)
	if valueFilterCol is not None:
		print ('Value filtering on column [%s].' % valueFilterCol)
	print('========================================\n')

	# Login through oauth (#6) - http://gspread.readthedocs.org/en/latest/oauth2.html
	json_key = json.load(open(oauthFile))
	scope = ['https://spreadsheets.google.com/feeds']

	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

	# Open the specified excel sheet and worksheet - http://gspread.readthedocs.org/en/latest/index.html
	gc = gspread.authorize(credentials)
	wks = gc.open(sheetName).worksheet(worksheet)

	while True:    # Read input forever
		barcode = raw_input("\nEnter the barcode: ")
		if barcode == "quit":
			break  # Exit the program

		print('Barcode is [%s].' % barcode)
		try:
			# Search filter by row/col/or nothing
			if searchFilterRow is not None:
				cell = _filterByRow(wks.findall(barcode), searchFilterRow)
			elif searchFilterCol is not None:
				cell = _filterByCol(wks.findall(barcode), searchFilterCol)
			else:
				cell = wks.find(barcode)
			print('Barcode found at row [%s] column [%s].' % (cell.row, cell.col))

			# Value filter by row/col/or nothing
			if valueFilterRow is not None:
				valueCell = wks.cell(valueFilterRow, cell.col)
			elif valueFilterCol is not None:
				valueCell = wks.cell(cell.row, valueFilterCol)
			else:
				valueCell = cell
			print('Value found is [%s].' % (valueCell.value))
		except CellNotFound:
			wks.add_rows(1)
			row_count = wks.row_count
			# Put the value in the value filter row
			if valueFilterCol is not None:
				col = valueFilterCol
			else:
				col = 1
			wks.update_cell(row_count, col, barcode)
			# TODO: Determine if we want to print out where the cell was added
			# cell = wks.find(barcode)
			# print('Barcode added at row [%s] column [%s].' % (cell.row, cell.col))

if __name__ == "__main__":
    main()

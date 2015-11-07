"""
pi-scanner
Barcode scanner project for the Raspberry Pi.
"""

import sys, argparse
import json
import gspread
from gspread.exceptions import CellNotFound
from oauth2client.client import SignedJwtAssertionCredentials

def main(argv):
	parser = argparse.ArgumentParser(description='pi-scanner - Barcode scanner project for the Raspberry Pi.', prefix_chars='-')
	parser.add_argument('-i', dest='oauthFile', action='store', required=True, help='OAuth file.')
	parser.add_argument('-sn', dest='sheetName', action='store', required=True, help='The name of the excel sheet.')
	
	args = parser.parse_args()
	
	if not args.oauthFile:
		parser.print_help()
		Sys.exit(2)
	if not args.sheetName:
		parser.print_help()
		Sys.exit(2)
	
	oauthFile = args.oauthFile
	sheetName = args.sheetName
	
	print('Input file is [%s].' % oauthFile)
	print('Sheet name is [%s].' % sheetName)
	
	json_key = json.load(open(oauthFile))
	scope = ['https://spreadsheets.google.com/feeds']
	
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
	
	gc = gspread.authorize(credentials)
	
	wks = gc.open("Test Sheet 1").sheet1
	
	print('Cell A1 is [%s].' % wks.acell('A1').value)
	print('Cell A2 is [%s].' % wks.acell('A2').value)
	print('Cell B1 is [%s].' % wks.acell('B1').value)
	print('Cell B2 is [%s].' % wks.acell('B2').value)
		
	while True:    # Read input forever
		barcode = raw_input("Enter the barcode: ")
		if barcode == "quit":
			break  # Exit the program

		print('Barcode is %s \n' % barcode)
		try:
			cell = wks.find(barcode)
			print('Barcode found at row %s column %s' % (cell.row, cell.col))
		except CellNotFound:
			wks.add_rows(1)
			row_count = wks.row_count
			wks.update_cell(row_count, 1, barcode)
			cell = wks.find(barcode)
			print('Barcode added at row %s column %s' % (cell.row, cell.col))


if __name__ == "__main__":
    main(sys.argv[1:])

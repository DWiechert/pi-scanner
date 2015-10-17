"""
pi-scanner
Barcode scanner project for the Raspberry Pi.
"""

import sys, getopt
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def main(argv):
	oauthFile = ''
	try:
		opts, args = getopt.getopt(argv,"i:",["ifile="])
	except getopt.GetoptError:
		print 'pi-scanner.py -i <oauth file>'
		sys.exit(2)
			
	for opt, arg in opts:
		if opt in ("-i", "--ifile"):
			oauthFile = arg		
	
	print 'Input file is "', oauthFile
	
	json_key = json.load(open(oauthFile))
	scope = ['https://spreadsheets.google.com/feeds']
	
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
	
	gc = gspread.authorize(credentials)
	
	wks = gc.open("Test Sheet 1").sheet1
	
	while True:    # Read input forever
		barcode = raw_input("Enter the barcode: ")
		if barcode == "quit":
			break  # Exit the program
		else:
			print('Barcode is %s \n' % (barcode))

if __name__ == "__main__":
    main(sys.argv[1:])

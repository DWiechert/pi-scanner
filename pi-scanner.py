"""
pi-scanner
Barcode scanner project for the Raspberry Pi.
"""

def main():
    while True:    # Read input forever
    	barcode = raw_input("Enter the barcode: ")
    	if barcode == "quit":
    	    break  # Exit the program
    	else:
    	    print('Barcode is %s \n' % (barcode))

if __name__ == "__main__":
    main()

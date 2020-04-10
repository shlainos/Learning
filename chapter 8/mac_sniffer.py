import scapy.all as s
import string
import os, sys

MY_MAC = '50:e5:49:c9:20:3e'
MAC_ADDRESSES = []
ERROR_CODE = -1
SUCCESS_CODE = 0

def is_valid_mac (mac_address):

	mac_bytes = mac_address.split (':')
	for byte in mac_bytes:
		b1 = byte[0]
		b2 = byte[1]
		if (b1 not in string.hexdigits and not b1.isdigit()) or (b2 not in string.hexdigits and not b2.isdigit()):

			print ("Invalid mac address")
			return ERROR_CODE

	print ("Valid mac address, vendor ID: {}".format (mac_address[0:8]))

	return SUCCESS_CODE


def print_source_address (frame):

	mac_addr = frame[s.Ether].src
	if mac_addr not in MAC_ADDRESSES:
		MAC_ADDRESSES.append (mac_addr)
		print (mac_addr)

	return


def filter_mac (frame):

	return s.Ether in frame and frame[s.Ether].dst == MY_MAC


def main():

	if len (sys.argv) >= 2:
		is_valid_mac (sys.argv[1])

	frames = s.sniff (count = 10, lfilter = filter_mac, prn = print_source_address)
	print (MAC_ADDRESSES)

	return


if __name__ == '__main__':
	main()
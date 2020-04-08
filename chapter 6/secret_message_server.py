from scapy.all import *
import socket
import os, sys

SERVER_IP = '0.0.0.0'
OUTPUT_STR = ''

def udp_packet (packet):

	return UDP in packet and Raw not in packet


def handle_udp_packet (udp_packet):

	port = udp_packet[UDP].dport
	letter = chr (port)
	try:
		if letter.isalpha():
			OUTPUT_STR += letter
			print (OUTPUT_STR)
	
	except Exception as e:
		pass

	return


def main():
	
	print ("UDP server, starts sniffing..\n")
	while True:
		packet = sniff (lfilter = udp_packet, prn = handle_udp_packet)

	print ("The string is: {}".OUTPUT_STR)
	return


if __name__ == '__main__':
	main()
from scapy.all import *
import time

MIN_PORT = 20
MAX_PORT = 1024
OUTPUT_MESSAGE = 'Open port: {}\n'

def main():
	
	dest_ip = input ("Please enter a destination domain address\n")
	print ("Scanning..\n")
	
	ports = list(range(MIN_PORT,MAX_PORT+1))
	for port in ports:
		syn_packet = IP (dst = dest_ip) / TCP (dport = port, seq = 123, flags = 'S')
		packet_response =  sr1(syn_packet, timeout = 0.2, verbose = False)
		if packet_response != None:
			if TCP in packet_response and packet_response[TCP].flags == 'SA':
				print (OUTPUT_MESSAGE.format (port))

	print ("Finished scanning")
	return


if __name__ == '__main__':
	main()

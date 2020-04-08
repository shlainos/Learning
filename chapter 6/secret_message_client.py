from scapy.all import *
import socket
import os, sys

SERVER_IP = '127.0.0.1'
CLIENT_IP = '0.0.0.0'
CLIENT_PORT = 8200

def main():

	data = ''.encode ()
	secret = input ("Please enter a secret message\n")
	ports = list (map (ord, list(secret)))
	# client_socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)

	for port in ports:
		pkt = IP (src = CLIENT_IP, dst = SERVER_IP) / UDP (sport = CLIENT_PORT, dport = port)
		send (pkt)
		# client_socket.sendto (data, (SERVER_IP,port))
		print ("Sent NULL to port {}".format (port))

	# client_socket.close()
	return


if __name__ == '__main__':
	main()
import socket
import sys, os

IP = '0.0.0.0'
PORT = 8821

def main():
	
	server_socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.bind((IP,PORT))
	print ("UDP server is ON")

	while True:
		(data, client_address) = server_socket.recvfrom (1024)
		if (data.decode () == 'EXIT'):
			server_socket.sendto ('ByeBye'.encode(), client_address)
			break

		data = ('Hello ' + data.decode()).encode()
		server_socket.sendto (data, client_address)

	server_socket.close()
	return

if __name__ == '__main__':
	main()
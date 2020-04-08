import socket
import time

# IP = 'networks.cyber.org.il'
IP = '127.0.0.1'
PORT = 8821


def main():

	client_socket = socket.socket (socket.AF_INET,socket.SOCK_DGRAM)
	
	while True:
		data = input ("Please enter a name\n").encode()
		sent_time = time.time()
		client_socket.sendto (data, (IP,PORT))
		(data, remote_address) = client_socket.recvfrom (1024)
		received_time= time.time()
		time_difference = received_time-sent_time

		print ("Received data: {0}\nFrom: {1}".format(data.decode(),remote_address))
		print ("Time difference: {} ms\n".format (time_difference*1000))

	client_socket.close()
	return


if __name__ == '__main__':
	main()
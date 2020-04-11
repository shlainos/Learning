import socket

IP = '127.0.0.1'
PORT = 23

client_socket = socket.socket()
client_socket.connect ((IP,PORT))

while True:

	user_name = input ("AAAK! My name is?\n") . encode ()
	client_socket.send (user_name)
	print ("Sent succesfully")
	data = client_socket.recv (1024) . decode()
	print ("Received: {}".format (data))
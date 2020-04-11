import socket
import select

def send_waiting_messages (wlist):

	for message in messages_to_send:
		(client_socket, data) = message
		if client_socket in wlist:
			client_socket.send (data.encode())
			messages_to_send.remove (message)

IP = '0.0.0.0'
PORT = 23

server_socket = socket.socket()
server_socket.bind ((IP,PORT))
server_socket.listen (5)

open_client_sockets = []
messages_to_send = []

while True:
	rlist, wlist, xlist = select.select ([server_socket] + open_client_sockets, open_client_sockets, [])
	for current_socket in rlist:
		if current_socket is server_socket:
			(new_socket, address) = server_socket.accept()
			open_client_sockets.append (new_socket)
		else:
			print ("New data from client~")
			data = current_socket.recv (1024) . decode()
			if data == '': # closed connection
				open_client_sockets.remove (current_socket)
				print ("Connection with client closed.")
			else:
				messages_to_send.append ((current_socket, 'Hello ' + data))
				print (data)

	send_waiting_messages (wlist)
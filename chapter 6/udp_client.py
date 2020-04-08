import socket

IP = 'networks.cyber.org.il'
PORT = 8821

data = 'my name is meow~'.encode ()

client_socket = socket.socket (socket.AF_INET,socket.SOCK_DGRAM)
client_socket.sendto (data, (IP,PORT))
(data, remote_address) = client_socket.recvfrom (1024)

print ("Received data: {0}\nFrom: {1}\n".format(data.decode(),remote_address))

client_socket.close()

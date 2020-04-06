import socket
import base64

HOST = 'networks.cyber.org.il'
PORT = 587

MAIL = 'GGWPITAYPWNS@gmx.com'
PASSWORD = 'MyPassMate'

s = socket.socket()
s.connect ((HOST,PORT))
data = s.recv (1024)
print (data)

message = 'EHLO\r\n'.encode ('ascii')
s.send (message)
data = s.recv (1024)
print (data)

encodedStr = 'AGZydXN0YUBnbXguY29tAFBhc3N3b3JkMSE=' # the given input mail
send_message = ('AUTH PLAIN '+ encodedStr + '\r\n').encode ('ascii')
data = s.send (send_message)
data = s.recv (1024)
print (data)

send_message = ('MAIL FROM:<frusta@gmx.com>'+ '\r\n').encode ('ascii')
data = s.send (send_message)
data = s.recv (1024)
print (data)

send_message = ('RCPT TO:resha@bads.com\r\n').encode ('ascii')
data = s.send (send_message)
data = s.recv (1024)
print (data)

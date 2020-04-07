from scapy.all import *
import socket
import sys,os


FLUSH_DNS_COMMAND = 'ipconfig /flushdns'
PATH_TO_DB = 'database.txt'
# REDIRECTION_IP_ADDRESS = '88.88.88.88'
REDIRECTION_IP_ADDRESS = socket.gethostbyname('www.facebook.com')
MY_IP_ADDRESS = '0.0.0.0'
MY_DNS_SERVER_PORT = 53

def handle_packet (packet):
	
	wanted_domain_name = packet[DNSQR].qname
	with open (PATH_TO_DB, 'r') as f:
		data = f.read()

	print (packet[DNS].show())
	print (data)

	# need to read ip address from the db, or just do DNS spoofing

	type_ = packet[DNSQR].qtype
	class_ = packet[DNSQR].qclass
	dns_response = DNSRR (rrname = wanted_domain_name, rdata = REDIRECTION_IP_ADDRESS, ttl = 150, rclass= class_, type = type_)
	dns_to_send = packet[DNS] # copy the sender's packet
	dns_to_send.an = dns_response
	dns_to_send.qr = 1 # change to query response
	dns_to_send.ra = 1 # recursion available, i dont think its criticall
	dns_to_send.ancount = 1
	dns_to_send.nscount = 0
	dns_to_send.arcount = 0

	response_packet = IP (src = packet[IP].dst, dst = packet[IP].src) / UDP (sport = packet[UDP].dport, dport = packet[UDP].sport) / dns_to_send
	
	print (response_packet[DNS].show())
	send (response_packet)

	return


def filter_dns (packet):
	# 
	return (DNS in packet and packet[DNS].opcode == 0 and packet[DNS].qr == 0 and packet[DNSQR].qtype ==1) # opcode = 0 means query, qr = 0 means asking for answer, qtype = 1 means A, and not PTR


def main():

	dns_server_socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
	dns_server_socket.bind ((MY_IP_ADDRESS,MY_DNS_SERVER_PORT))

	c = {'www.google.com': ['A', socket.gethostbyname('www.facebook.com'), 64]} # to delete
	with open (PATH_TO_DB,'w') as f:
		f.write (str (c))

	os.system (FLUSH_DNS_COMMAND)
	print ("Server starts sniffing..\n")
	while True:
		packet = sniff (count = 50, lfilter = filter_dns, prn = handle_packet)
	
	return


if __name__ == '__main__':
	main()
from scapy.all import *
import sys, os
import socket


FLUSH_DNS_COMMAND = 'ipconfig /flushdns'

def print_raw_data (tcp_packet):

	try:
		print (tcp_packet[Raw])

	except Exception as ex:
		pass
	
	return

def print_packet (packet):

	print (packet.show())
	return


def print_query_name (dns_packet):

	print (dns_packet[DNSQR].qname)
	return


def filter_facebook_packet (packet):

	FACEBOOK_IP = socket.gethostbyname('www.facebook.com')
	if IP not in packet:
		return False
	else:
		if packet[IP].dst == FACEBOOK_IP or packet[IP].src == FACEBOOK_IP:
			return True
		else:
			return False


def filter_http_request (packet):

	return (TCP in packet and packet[TCP].dport == 80)


def filter_tcp (packet):

	return TCP in packet


def filter_dns (packet):

	return (DNS in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype ==1) # opcode = 0 means query, qtype = 1 means A, and not PTR


def  main():

	# os.system (FLUSH_DNS_COMMAND)
	print ("Sniff started..\n")
	# packets = sniff (count = 10, lfilter = filter_dns, prn = print_query_name)
	# packets = sniff (count = 20, lfilter = filter_http_request, prn = print_raw_data)
	packets = sniff (count = 5, lfilter = filter_facebook_packet, prn = print_packet)
	# print (packets.summary())
	# my_packet = IP (dst = 'www.google.com')
	# my_packet[IP].src = '123.12.9.67' # Can even insert domain names!
	# my_packet.show()

	# new_packet = IP() / Raw ("MEOW I LOVE DATA!")
	# send (my_packet)
	
	return


if __name__ == '__main__':
	main()
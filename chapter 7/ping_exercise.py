import scapy.all as s

DEST_IP = 'www.facebook.com'
PADDING = 'Mega MCnuggets'

def main():

	icmp_packet = s.IP(dst = DEST_IP) / s.ICMP (id = 1, seq = 120) / PADDING
	icmp_response = s.sr1 (icmp_packet)
	print (icmp_response.show())

	icmp_packet = s.IP(dst = DEST_IP) / s.ICMP (id = 2, seq = 121) / PADDING
	icmp_response = s.sr1 (icmp_packet)
	print (icmp_response.show())
	
	return


if __name__ == '__main__':
	main()
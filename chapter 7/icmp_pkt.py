import scapy.all as s

DEST_IP = 'www.google.com'
DEST_PORT = 80
PADDING = 'Mega MCnuggets'

def main():

	icmp_packet = s.IP(dst = DEST_IP) / s.ICMP () / PADDING
	icmp_response = s.sr1 (icmp_packet)

	print (icmp_response.show())
	return
	

if __name__ == '__main__':
		main()	

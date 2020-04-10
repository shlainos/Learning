import scapy.all as s

DEFAULT_GATEWAY = '10.100.102.1'

def main():

	pkt = s.Ether () / s.IP (dst = DEFAULT_GATEWAY) / s.ICMP ()
	s.sendp(pkt)
	return


if __name__ == '__main__':
	main()
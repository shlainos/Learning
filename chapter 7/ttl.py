import scapy.all as s
import os, sys
import time

DEST_IP = 'www.google.com'
PADDING = 'Mega MCnuggets'
INIT_TTL = 1

def main():

	if len (sys.argv) < 2:
		print ("Invalid usage, please enter a wanted domain\n")
		sys.exit()

	DEST_IP = sys.argv[1]
	next_hop_pkt = s.IP() / s.ICMP ()

	i = INIT_TTL
	while next_hop_pkt[s.ICMP].type != 0:
		icmp_pkt = s.IP (dst = DEST_IP, ttl = i) / s.ICMP () / PADDING
		t1 = time.time()
		next_hop_pkt = s.sr1 (icmp_pkt, timeout = 0.5, verbose = False)
		t2 = time.time()
		time_diff = (t2 - t1) * 1000
		next_hop_ip = next_hop_pkt[s.IP].src
		print ("{}:\t{}ms\t{}".format (i, time_diff ,next_hop_ip))
		i += 1	

	print ("Destination IP is: {}, took {} ms".format (next_hop_pkt[s.IP].src, time_diff))

	return


if __name__ == '__main__':
	main()
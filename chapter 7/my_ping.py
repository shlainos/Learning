import scapy.all as s
import sys, os

PADDING = 'Mega MCnuggets'
INITIAL_ID = 1
INITIAL_SEQ = 120

def main():

	if len (sys.argv) < 2:
		print ("Invalid usage, please enter an argument\n")
		sys.exit()

	packets_num = 4
	DEST_IP = sys.argv[1]
	if len (sys.argv) == 3:
		packets_num = sys.argv[2]

	print ("Sending {0} packets to {1}".format (packets_num, DEST_IP))
	
	# counter = packets_num
	# for i in range (int(counter)):
	#	icmp_packet = s.IP(dst = DEST_IP) / s.ICMP (id = INITIAL_ID + i, seq = INITIAL_SEQ + i) / PADDING
	#	icmp_response = s.sr1 (icmp_packet,verbose = False, timeout = 0.2)
	#	if icmp_response == None:
	#		packets_num -= 1
	ID_S = []
	SEQ_S = []
	for i in range (1, int (packets_num) + 1):
		ID_S.append (INITIAL_ID + i)
		SEQ_S.append (INITIAL_SEQ + i)

	icmp_pkts = s.IP(dst = DEST_IP) / s.ICMP (id = 1, seq = SEQ_S) / PADDING
	ans, unans = s.sr (icmp_pkts, verbose = False, timeout = 0.5)

	print ("Received {} response packets".format (len (ans)))

	return
	

if __name__ == '__main__':
		main()	

from scapy.all import *

DEST_IP = 'www.google.com'
DEST_PORT = 80

def main():

	syn_segment = TCP(dport = DEST_PORT, seq = 123, flags = 'S')
	ip_segment = IP (dst = DEST_IP)
	my_packet = ip_segment / syn_segment
	packet_response = sr1(my_packet)
	seq_num = packet_response[TCP].seq
	ack_num = packet_response[TCP].ack
	#
	tcp_seg_length = len (packet_response[TCP].load)
	ack_segment = IP (dst = DEST_IP) / TCP (dport = DEST_PORT, seq = ack_num, ack = seq_num + 1 ,flags = 'A')
	send (ack_segment)

	return

if __name__ == '__main__':
	main()
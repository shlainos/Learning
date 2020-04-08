from scapy.all import *

WANTED_DOMAIN = 'www.google.com'
SOURCE_PORT = 8200
DNS_PORT = 53
DNS_SERVER_IP = '8.8.8.8'


def is_valid_ipv4_address(address):
    
    address = (str(address)) [1:]
    
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def main():
	
	requested_domain = input ('Please enter a valid domain name\n')
	# make dns query packet
	dns_packet = DNS (qdcount = 1)
	dns_question_record = DNSQR (qname = requested_domain)
	dns_packet.qd = dns_question_record

	udp_packet = UDP (sport = SOURCE_PORT,dport = DNS_PORT)
	ip_packet = IP (dst = DNS_SERVER_IP)

	dns_query_packet = ip_packet / udp_packet / dns_packet
	response_packet = sr1 (dns_query_packet)
	
	for i in range (response_packet.ancount):
		ip_data = (response_packet.an[i].rdata)
		if not is_valid_ipv4_address(ip_data):
			continue
		else:
			print ("IP address: {}".format (ip_data))
			break

	return


if __name__ == '__main__':
	main()
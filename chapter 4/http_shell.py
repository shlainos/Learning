# HTTP Server Shell
# Author: Itay
# Purpose: Provide a basis for Ex. 4.4

import datetime
import socket
import os, sys
from urllib.parse import urlparse, parse_qs

IP = '0.0.0.0'
PORT = 80
CHUNK = 65536
SOCKET_TIMEOUT = 10
DEFAULT_ERROR_MESSAGE = 'Invalid input\n'
DEFAULT_URL = '\\index.html'
HTTP_VERSION = 'HTTP/1.1 '
HTML_CONTENT = 'Content-Type: text/html; charset=utf-8\r\n'
JPG_CONTENT ='Content-Type: image/jpeg\r\n'
JS_CONTENT = 'Content-Type: text/javascript; charset=UTF-8\r\n'
CSS_CONTENT = 'Content-Type: text/css\r\n'
SERVER = 'Server: ITAY SERVER\r\n'

def mathematical_increment (num):
    
    if not num.isdigit():
        return '' 

    return str (int(num)+1)


def multiply_operation (height, width):
    
    if (not height.isdigit() or not width.isdigit()):
        return '' 

    else:
        return str (int(height) * int (width))


def new_session (client_socket, server_socket):
    
    client_socket.close()
    print ("Connection closed\nWaiting for a new connection..\n")
    client_socket, client_address = server_socket.accept()
    print ("New client was entered!\nsocket: {0}\naddress: {1}\n".format(client_socket,client_address))
    return client_socket, client_address


def get_file_data(filename):
    """ Get data from file """
    with open (filename, 'rb') as f:
        data = f.read()
    return data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if '?' in resource:
        parsed_url = urlparse (resource)
        params = parse_qs (parsed_url.query)
        resource = parsed_url.path
        # resource = resource[:resource.find('?')]
        print (resource)
        print (params)

    if resource == '\\':
        url = DEFAULT_URL
    elif resource == '\\favicon.ico':
        url = '\\imgs\\favicon.ico'
    # elif resource == '\\calculate-next'
    else:
        url = resource

    
    """
    # TO DO: check if URL had been redirected, not available or other error code. For example:
    if url in REDIRECTION_DICTIONARY:
        # TO DO: send 302 redirection response
    """
    filetype = url[url.rfind('.'):]
    
    status_line = HTTP_VERSION + '200 OK' + '\r\n'

    http_sub_header = SERVER
    if filetype == '.html':
        http_sub_header += HTML_CONTENT 

    elif filetype == '.jpg':
        http_sub_header += JPG_CONTENT

    elif filetype == '.js':
        http_sub_header += JS_CONTENT

    elif filetype == '.css':
        http_sub_header += CSS_CONTENT
    
    filename = os.getcwd() + url
    
    if os.path.isfile (filename):
        data = get_file_data(filename)
        data_size = len(data)
        http_sub_header += 'Content-Length: ' + str(data_size) + '\r\n'

    elif url == '\\calculate-next':
        data = int (mathematical_increment (params['num'][0]))
        data = str(data).encode()
        data_size = len(data)
        http_sub_header += 'Content-Type: ' + 'text/plain\r\n'
        http_sub_header += 'Content-Length: ' + str(data_size) + '\r\n'

    elif url == '\\calculate-area':
        data = multiply_operation (params['height'][0], params['width'][0])
        data = str(data).encode()
        data_size = len(data)
        http_sub_header += 'Content-Type: ' + 'text/plain\r\n'
        http_sub_header += 'Content-Length: ' + str(data_size) + '\r\n'
    
    else:
        status_line = HTTP_VERSION + '404 Not Found\r\n'
        data = ''.encode()

    http_header = status_line + http_sub_header + '\r\n'
    http_response = http_header.encode() + data
    client_socket.send (http_response)


def validate_http_request(raw_data):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # TO DO: write function
    splitted_data = raw_data.split('\r\n')
    request = splitted_data[0]
    splitted_request = request.split ()
    resource = None

    if len (splitted_request) != 3:
        return False, resource

    if splitted_request[0] != 'GET':
        return False, resource

    if splitted_request[2] [0:4]!= 'HTTP':
        return False, resource
    
    resource = raw_data.split('\r\n')[0].split()[1].replace ('/', '\\')

    return True, resource


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print ('Client connected')
    while True:
        # TO DO: insert code that receives client request
        # ...
        client_request = client_socket.recv (CHUNK).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print ('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print ('Error: Not a valid HTTP request')
            break
    print ('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print ("Listening for connections on port {}" .format (PORT) )

    while True:
        client_socket, client_address = server_socket.accept()
        print ('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
#!/usr/bin/python
import socket
import time

ip = "127.0.0.1"
port = 1102

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    with open('/tmp/mode', 'r') as f:
        line = f.readline().rstrip()
	print "LINE: |"+line+"|"
        if line == "boot":
            message = "GREEN\n"
        elif line == "eng":
            message = "RED\n"
        elif line == "prod":
            message = "YELLOW\n"
        elif line == "open":
            message = "ORANGE\n"
	else:
            message = "OFF\n"

        print "Message: "+message
        sock.sendto(message,(ip,port))
        time.sleep(1)

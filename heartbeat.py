#!/usr/bin/python
import socket
import time

ip = "127.0.0.1"
port = 1101

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
state = 0

while True:
    if state == 0:
        message = "OFF\n"
        state += 1
    elif state == 1:
        message = "GREEN\n"
        state += 1
    elif state == 2:
        message = "YELLOW\n"
        state += 1
    elif state == 3:
        message = "ORANGE\n"
        state += 1
    elif state == 4:
        message = "RED\n"
        state = 0

    print "Message: "+message
    sock.sendto(message,(ip,port))
    time.sleep(1)

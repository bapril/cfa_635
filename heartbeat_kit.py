#!/usr/bin/python
import socket
import time

ip = "127.0.0.1"
port = 1101

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
state = 0
color = "GREEN"
up = True
sock.sendto("OFF\n",(ip,port))

while True:
    if up == True:
        state += 25
        if state >= 100:
            state = 100
            up = False
    else:
        state -= 25
        if state < 1:
            if color == "RED":
                color = "GREEN"
            else:
                color = "RED"
            state = 0
            up = True
    if color == "RED":
        message = "0:"+str(state)+ "\n"
    else:
        message = str(state)+ ":0\n"
    print "Message: "+message
    sock.sendto(message,(ip,port))
    time.sleep(.5)

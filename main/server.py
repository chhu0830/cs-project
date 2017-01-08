#!/usr/bin/env python3
import socket
import netifaces as ni
import os
import sys
import datetime

if (len(sys.argv) != 3):
    print("usage:", sys.argv[0], "<net interface> <port>")
    sys.exit()

TCP_IP = ni.ifaddresses(sys.argv[1])[2][0]['addr']
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("listen at", TCP_IP, TCP_PORT)

data = {}
danger_distance = 20.0
danger_speed = 100.0
low_speed = 10.0

while True:
    conn, addr = s.accept()
    print('Connection address:', addr)

    recv = conn.recv(BUFFER_SIZE)
    recv = recv.decode()
    recv = recv.split(' ')
    data[recv[0]] = [recv[1], recv[2]]

    cur_speed = recv[1]
    cur_distance = recv[2]
    
    max_speed = 0.0
    for i in data:
        if float(data[i][0]) > max_speed:
            max_speed = float(data[i][0])

    if float(cur_distance) < danger_distance:
        msg = "SLOW"
    elif float(cur_speed) > danger_speed:
        msg = "SLOW"
    elif float(cur_speed) < max_speed:
        msg = "FAST"
    elif float(cur_speed) < low_speed:
        msg = "FAST"
    else:
        msg = "KEEP"

    conn.send(msg.encode('utf-8'))
    conn.close()

    f = open('log/' + recv[0], 'a')
    f.write(str(datetime.datetime.now()) + '\t' + cur_speed + '\t' + cur_distance + '\t' + msg + '\n')
    f.close()
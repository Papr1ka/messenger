#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os

sock = socket.socket()
sock.bind(('0.0.0.0', 8000))
sock.listen(0)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    try:
    	data = conn.recv(1024)
    	if not data:
    		break
    	conn.send(data.upper())
    except ConnectionResetError:
    	print("отключился")
conn.close()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os

sock = socket.socket()
sock.bind(('0.0.0.0', int(os.environ.get("PORT"))))
sock.listen()

while True:
    try:
    	conn, addr = sock.accept()
    	print('connected:', addr)
    	data = conn.recv(1024)
    	if not data:
    		break
    	conn.send(data.upper())
    except ConnectionResetError:
    	print("отключился")

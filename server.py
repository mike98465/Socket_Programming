import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-ip', '--ip', required=True,
                help = 'ip address')
ap.add_argument('-p', '--port', required=True,
                help = 'port number')
args = ap.parse_args()
 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

HOST=args.ip
PORT=int(args.port)

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

c,addr = s.accept()
print('Connected to :', addr[0], ':', addr[1]) 

data = b""
payload_size = struct.calcsize(">L")

while(1):
	while len(data) < payload_size:
		print("Recv: {}".format(len(data)))
		data += c.recv(4096)

	print("Done Recv: {}".format(len(data)))
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack(">L", packed_msg_size)[0]
	print("msg_size: {}".format(msg_size))

	while len(data) < msg_size:
		data += c.recv(4096)

	frame_data = data[:msg_size]
	data = data[msg_size:]

	frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
	frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
	
	cv2.imshow("Socket_Programming",frame)
	
	if cv2.waitKey(1) == 13:
		break
	
c.close() 
cv2.destroyAllWindows()
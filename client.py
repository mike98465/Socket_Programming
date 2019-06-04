import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import threading
import numpy as np
from PIL import Image

import imutils

ap = argparse.ArgumentParser()
ap.add_argument('-ip', '--ip', required=True,
                help = 'ip address')
ap.add_argument('-p', '--port', required=True,
                help = 'port number')
args = ap.parse_args()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((args.ip, args.port))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

#cam.set(3, 320);
#cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

ret, frame = cam.read()
#frame = imutils.resize(frame, width=500)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)
firstFrame = gray

while True:
    ret, frame = cam.read()
    #frame = cv2.flip(frame, -1)    
  
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    #data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)

    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()

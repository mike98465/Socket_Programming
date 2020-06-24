'''
MIT License
Copyright (c) 2017 Kittinan
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

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

ip = ''

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('ip', 8485))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

ret, frame = cam.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)
firstFrame = gray

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, -1)    
    '''
    gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    #gray1 = cv2.blur(gray1,(21,21),0)
    gray1 = Image.fromarray(gray1,'L')

    gray2 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #gray2 = cv2.blur(gray2,(21,21),0)
    gray2 = Image.fromarray(gray2,'L')

    pairs = zip(gray1.getdata(),gray2.getdata())

    if len(gray1.getbands()) == 1:
        #for grayscale img
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
    
    ncomponents = gray1.size[0] * gray1.size[1] * 3
        
    #print(str((dif / 255.0 *100)/ ncomponents) + "%")
    '''
    # resize the frame, convert it to grayscale, and blur it
    #frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
    # if the first frame is None, initialize it
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    print(sum(sum(thresh))/thresh.shape[0]/thresh.shape[1])
    firstFrame = gray    
    img1 = frame

    #frame = cv2.flip(frame, -1)
    #if (dif / 255.0 *100)/ ncomponents >= 1:
    if  sum(sum(thresh))/thresh.shape[0]/thresh.shape[1] > 0:
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        #data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1

cam.release()

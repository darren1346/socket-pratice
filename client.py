# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:56:01 2020

@author: e420
"""

# FOR CLIENT SEND 
import socket
import cv2
#拍照
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
i = "TEST"
while True :
    _,img = cap.read()
    cv2.imshow("frame",img)
    key = cv2.waitKey(1)
    cv2.imwrite('C:/Users/e420/Desktop/soc/'+i+'.jpeg', img)
    print ("img is saved")
    break
cap.release()
cv2.destroyAllWindows()

#CONNECT TO SERVER
c = socket.socket()
q = "192.168.0.109"
p = 1334
c.connect((q,p))
path = "C:/Users/e420/Desktop/soc/TEST.jpeg"
image = open(path,"rb")
print(c)
#if c != 0:
while True:
    for i in image:
        c.send(i)
    break
c.close()

q1 = "192.168.0.109"
q2 = 1234
s = socket.socket()
s.connect((q1,q2))
result = s.recv(1)
result = int (result)
print (result)
c.close()
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:39:26 2020

@author: darre
"""

#This is for SERVER GET
import socket
import cv2
import numpy as np

#socket connect
c = socket.socket()
ip  = "192.168.0.109"
port  = 1334
s = socket.socket()
s.bind((ip,port))
s.listen(1)
c,address = s.accept()
condition = True
s = "TEST.jpeg" 
f = open(s,"wb")

#send image
while condition:
    image = c.recv(1024)
    if str(image) == "b''" :
        condition = False
    f.write(image)

    #start object detection
# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
ans = 0
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
# Loading image
img = cv2.imread("TEST.jpeg")
img = cv2.resize(img, None, fx= 1, fy= 1)
height, width, channels = img.shape
# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)
# Showing informations on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        print("detect")
        if label == "person":
            ans = 1 
            '''c.send(1)
        else:
            c.send(0)'''
print (ans)
c.close()
print("close")


#測試 第二次連接並傳送結果
nexts = socket.socket()
q = "192.168.0.109"
p = 1234
nexts.bind((q,p))
nexts.listen(1)
c,address = nexts.accept()
print("reconnecting...")
print(ans)
ans = str(ans)
ans = ans.encode()
c.send(ans)
nexts.close()
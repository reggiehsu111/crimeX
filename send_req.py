import requests

import cv2

cap = cv2.VideoCapture(0)
num = 0
while 1:

    cap = cv2.VideoCapture(0)
    ret, image = cap.read()


    #saving image to current folder
    picName = 'pic'+str(num)+'.png'
    cv2.imwrite(picName, image)
    num = num+1

    with open(picName, 'rb') as f:
    	r = requests.post("http://0.0.0.0:5000/upload", data={picName: f})
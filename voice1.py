
import threading
import os
from os import path
import json
import requests
import cv2
import numpy as np
import base64
import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS
import time
import re


#time of audio chunks
process_time = 2

#audio clips ready for processing
audio_list = []

#language of dectection
fromLanguage = "zh-tw"

#instatiate speech recognizer
r=sr.Recognizer()

#weighted average of vision and speech confidence
prediction = 0

#variable for counting the number of 救命s appearing in google api's prediction
flag = 0

#the confidence of detecting 救命
speech_conf = 0

#the confidence of computer vision detecting required moves
yes_conf = 0

#instantiating lock
lock = threading.Lock()

#couting weighted average using lock method
def predict():
    global prediction 
    lock.acquire()
    try:
        prediction = yes_conf*0.3+speech_conf*0.7*flag
        print("prediction: "+ str(prediction)) 
        print("yes_conf: "+str(yes_conf))
        print("speech_conf: "+str(speech_conf))
    finally:
        lock.release()

#asking azure api for custom vision prediction
class vision():

    def __init__(self):
        self.training_key = "6c96d345fce740cabb19288e675aa798"
        self.prediction_key = "c14b65fd6278419baadad461d56747d1"
        self.projectid = "29f7efe7-adfb-43d9-a7af-70d9f9a2b1de"

        self.headers = {'Prediction-key': "c14b65fd6278419baadad461d56747d1","Content-Type": "application/octet-stream"}


    def capture_image(self):
        self.cap = cv2.VideoCapture(0)
            # Capture frame-by-frame
        ret, frame = cap.read()

    def vision_main(self):
        global yes_conf
        while 1:

            cap = cv2.VideoCapture(0)
            num = 0
            ret, image = cap.read()

            retval, buffer = cv2.imencode('.jpg', image)

            #converting image to byte form
            buff = base64.b64encode(buffer)

            #saving image to current folder
            picName = 'pic'+str(num)+'.png'
            cv2.imwrite(picName, image)


            #open saved image
            path_to_file="./"+picName
            with open(path_to_file, 'rb') as f:
                data1 = f.read()

            #getting response
            response = requests.request('POST',"https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Prediction/29f7efe7-adfb-43d9-a7af-70d9f9a2b1de/image?iterationId=6a2647cb-dfe9-4699-b723-33e06f667c5e"
                                            ,headers=self.headers, data=data1)
            response.raise_for_status()
            analysis = response.json()

            #getting yes and no confidence and their probabilities
            yes_conf = analysis['Predictions'][0]['Probability']
            no_conf = analysis['Predictions'][1]['Probability']
            tag1 = analysis['Predictions'][0]['Tag']
            tag2 = analysis['Predictions'][1]['Tag']

            #update prediction
            predict()
            print(tag1 + ": " + str(yes_conf))
            print(tag2 + ": " + str(no_conf))
            # print(analysis)

            #
            time.sleep(2)


def start_vision():
    Vision = vision()
    Vision.vision_main()


def speech_main():
#    with sr.AudioFile("./Voice0047.wav") as source:
    while 1:
        # print(sr.Microphone())
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("start speaking")
            audio=r.listen(source,None,process_time)
            audio_list.append(audio)
            # print(audio_list)
        print("recognizing")
    return

def process_text():
    global speech_conf, flag
    help_arr = ["救命","九妹","啾咪"]
    while 1:
        if len(audio_list)!=0:
            audio1 = audio_list.pop()
            #print(audio1)
            # print("after processing text: " + str(audio_list))
            txt=r.recognize_google(audio1,language=fromLanguage,show_all=True)
            if len(txt)!=0:
                print("text: "+ str(txt))
                # 
                print(type(txt))
                flag = 0
                for return_num in range(min(3,len(txt['alternative']))):
                    if any(re.findall('|'.join(help_arr),txt['alternative'][return_num]["transcript"])):
                        print("SOS!!")
                        flag = flag+1
                    elif txt['alternative'][return_num]["transcript"].find("救命") == -1:
                        print("not detected")
                print("flag: " + str(flag))
                predict()
                speech_conf = txt['alternative'][0]["confidence"]
                print(txt['alternative'][0]["confidence"])
                # print(type(txt['alternative'][0]["transcript"]))



class Thread(threading.Thread):
    def __init__(self,  t, daemon, *args):
        threading.Thread.__init__(self,  target=t, args=args)
        self.setDaemon(daemon)
        self.start()

    # def join(self):
    #     self.join()
if __name__ == '__main__':
    t1 = Thread(speech_main, True)
    t2 = Thread(process_text, True)
    t3 = Thread(start_vision, True)
    time.sleep(1)
    t4 = Thread(start_vision, True)



    # t4 = threading.Thread(target=process_text)
    # t1.start()
    # t2.start()
    # t3.start()


    t2.join()
    t3.join()
    t4.join()
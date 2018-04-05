
import threading
import os
from os import path
import json

import speech_recognition as sr
from textblob import TextBlob

from gtts import gTTS
import time
import vision_withurl

process_time = 2
audio_list = []
fromLanguage = "zh-tw"
r=sr.Recognizer()


def start_vision():
    Vision = vision_withurl.vision()
    Vision.main()

def main():
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
                	if txt['alternative'][return_num]["transcript"].find("救命") != -1:
                		print("SOS!!!!")
                        flag ++
                	elif txt['alternative'][return_num]["transcript"].find("救命") == -1:
                		print("not detected")
                print(txt['alternative'][0]["confidence"])
                print(type(txt['alternative'][0]["transcript"]))


t1 = threading.Thread(target=main)
t2 = threading.Thread(name = "t2", target=process_text)
t3 = threading.Thread(name="t3", target = start_vision)

t2.setDaemon(True)
t3.setDaemon(True)

# t4 = threading.Thread(target=process_text)
t1.start()
t2.start()
t3.start()


t2.join()
t3.join()


	

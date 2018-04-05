
import threading
import os
from os import path
import json

import speech_recognition as sr
from textblob import TextBlob

from gtts import gTTS
import vision_withurl



Vision = vision_withurl.vision()
def main():
    fromLanguage = "zh-tw"
    r=sr.Recognizer()
#    with sr.AudioFile("./Voice0047.wav") as source:
    print(sr.Microphone())
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) 
        print("start speaking")
        audio=r.listen(source, None, 4)
        print(audio)
    print("recognizing")
    txt=r.recognize_google(audio,language=fromLanguage,show_all=True)
    print(txt)
    if (len(txt)!=0):
        print(len(txt['alternative']))
        for return_num in range(min(3,len(txt['alternative']))):
            if txt['alternative'][return_num]["transcript"].find("救命") != -1:
                print("SOS!!!!")
            elif txt['alternative'][return_num]["transcript"].find("救命") == -1:
                print("not detected")
        print(txt['alternative'][0]["confidence"])
        print(type(txt['alternative'][0]["transcript"]))
    return

while True:
    main()

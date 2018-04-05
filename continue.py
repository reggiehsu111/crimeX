#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time

import speech_recognition as sr

fromLanguage = "zh-tw"
# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("recognizing")
        print(audio)
        txt=recognizer.recognize_google(audio,language=fromLanguage,show_all=True)
        print(txt)
        print(type(txt))
        print(len(txt['alternative']))
        for return_num in range(min(3,len(txt['alternative']))):
            if txt['alternative'][return_num]["transcript"].find("救命") != -1:
                print("SOS!!!!")
            elif txt['alternative'][return_num]["transcript"].find("救命") == -1:
                print("not detected")
        print(txt['alternative'][0]["confidence"])
        print(type(txt['alternative'][0]["transcript"]))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
print(m)
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
print("listening")
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds

for _ in range(50): 
    time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=False)
print("stops listening")



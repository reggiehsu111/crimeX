import video_withurl
import voice1

def start_vision():
    Vision = vision_withurl.vision()
    Vision.vision_main()

t1 = Thread(speech_main, True)
t2 = Thread(process_text, True)
t3 = Thread(start_vision, True)
time.sleep(1)
t4 = Thread(start_vision, True)
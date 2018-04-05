import requests
from picamera import PiCamera
#import cv2
import numpy as np
import base64
import time

yes_conf = 0
class vision():
	def __init__(self):
		self.training_key = "6c96d345fce740cabb19288e675aa798"
		self.prediction_key = "c14b65fd6278419baadad461d56747d1"
		self.projectid = "29f7efe7-adfb-43d9-a7af-70d9f9a2b1de"

		self.headers = {'Prediction-key': "c14b65fd6278419baadad461d56747d1","Content-Type": "application/octet-stream"}


	#def capture_image(self):
		#self.cap = cv2.VideoCapture(0)
			# Capture frame-by-frame
		#ret, frame = cap.read()

	def vision_main(self):
		global yes_conf
		camera = PiCamera()
		while 1:

			#cap = cv2.VideoCapture(0)
			num = 0
			#ret, image = cap.read()
			#retval, buffer = cv2.imencode('.jpg', image)
			#buff = base64.b64encode(buffer)
			picName = 'pic'+str(num)+'.jpg'
			camera.capture('/home/pi/Desktop/'+picName)
			#cv2.imwrite(picName, image)
			path_to_file= '/home/pi/Desktop/'+picName
			with open(path_to_file, 'rb') as f:
				data1 = f.read()
			#print(len(data1))
			response = requests.request('POST',"https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Prediction/29f7efe7-adfb-43d9-a7af-70d9f9a2b1de/image?iterationId=6a2647cb-dfe9-4699-b723-33e06f667c5e"
											,headers=self.headers, data=data1)
			response.raise_for_status()
			analysis = response.json()
			yes_conf = analysis['Predictions'][0]['Probability']
			no_conf = analysis['Predictions'][1]['Probability']
			tag1 = analysis['Predictions'][0]['Tag']
			tag2 = analysis['Predictions'][1]['Tag']


			print(tag1 + ": " + str(yes_conf))
			print(tag2 + ": " + str(no_conf))
			# print(analysis)
			time.sleep(2)

if __name__ == "__main__":
	Vision = vision()
	Vision.vision_main()


from flask import Flask
from PIL import Image

app = Flask(__name__)

@app.route('/')
def root():
    return 'root'

@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	image = Image.open(file)
	image.show() 

if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0', threaded=True, debug=False)
	except KeyboardInterrupt:
		print('Interrupt, Exiting...')
	finally:
		print('Exiting...')
		exit(-1)



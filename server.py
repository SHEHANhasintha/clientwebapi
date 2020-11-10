from flask import Flask
from flask import request, jsonify
from markupsafe import escape
from PIL import Image

import numpy
import requests
from pprint import pprint
import time
import json



#import logger
app = Flask(__name__)




@app.route('/')
def hello_World():
	return 'Hello World'

#@app.route('/images/<st>')

@app.route('/images/<username>',methods=['GET','POST','DELETE','PATCH'])
def show_user_profile(username):
	if request.method == 'GET':
		#print(request.args)
		# show the user profile for that user
		#return 'User'
		data = "getting info"
		return jsonify(isError= False,
					message= "Success",
					data=data,
					statusCode= 200), 200

	if request.method == 'POST':

		if ("image" in request.files):
			

			image  = Image.open(request.files["image"])
			print(image.format)
			if (image.format == "JPEG"):
				image = image.resize((10,10))
				
				image.save("received\\received.jpg")

				isError=True;
				print("file process is completed")

				image_np = numpy.array(image)
				payload = {"instances": [image_np.tolist()]}
				start = time.perf_counter()
				res = requests.post("http://ec2-54-196-1-250.compute-1.amazonaws.com/v1/models/default:predict", json=payload)
				print(res.status_code)
				data = "ok image was taken"


				if (res.status_code == 200):
					message =  "Success"
					res = res.json()["predictions"][0]["detection_classes"][0]

					isError = False
					statusCode = 200
				else:
					res = None
					message = "image is too big"
					statusCode = 400

				#json_object = json.dumps(res.json())
				#with open("response.json", "w") as outfile: 
				#	outfile.write(json_object) 
			else:
				message = "Request Failed invalid file format"
				res = None
				statusCode = 400

		else:
			isError = True
			statusCode = 400
			res = None
			data = "An image input is required"
		
		return jsonify(isError=isError,
					message= message,
					data=data,
					res = res,
					statusCode= statusCode), 200


@app.route('/post/<int:post_id>')
def show_post(post_id):
	return 'post %d' % post_id


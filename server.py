from flask import Flask
from flask import request, jsonify
from PIL import Image
import io

import numpy
import requests
import time
import json

from database.dataBase import Database
from imageRec.imgRec import ImageRec

app = Flask(__name__)

db = Database();

@app.route('/')
def hello_World():
	return jsonify(isError="false",
				message= "Hello spam logo detector",
				statusCode= 200), 200


@app.route('/images',methods=['GET','POST','DELETE','PATCH'])
def show_user_profile():
	if request.method == 'GET':
		data = "getting info"
		return jsonify(isError= False,
					message= "Success",
					data=data,
					statusCode= 200), 200

	if request.method == 'POST':
		if ("image" in request.files):
			image  = Image.open(request.files["image"])
			#print(image.format)
			if (image.format == "JPEG"):
				imageOriginal = image
				image.save("received\\received.jpg")
				image = image.resize((10,10))

				isError=True;
				print("file process is completed")
				image_np = numpy.array(image)
				payload = {"instances": [image_np.tolist()]}
				start = time.perf_counter()
				originalDataResponce = requests.post("http://ec2-54-196-1-250.compute-1.amazonaws.com/v1/models/default:predict", json=payload)
				print(originalDataResponce.status_code)
				data = "ok image was taken"

				if (originalDataResponce.status_code == 200):
					message =  "Success"
					pred = originalDataResponce.json()["predictions"][0]["detection_classes"][0]

					images = db.getEveryDisp()
					res = 'nomatch'
					count = 1;
					for img in images:
						print(int(count)==int(pred))
						if (int(count) == int(pred)):
							imagePri = Image.open(io.BytesIO(db.getImage(img['name'])))
							imagePri.save(('received\\' + img['name'] + '.jpg'))
							width, height = imagePri.size
							print(width,height)

							imageReceved = imageOriginal.resize((width, height))
							imageReceved.save("received\\received.jpg")


							ImageR = ImageRec(('received\\' + img['name'] + '.jpg'), "received\\received.jpg");
							if (ImageR.estimate() > 0.1):
								res = {"logoName": img['name'], "proberbility": ImageR.estimate()}
								break;
						count+=1


					isError = False
					statusCode = 200
				else:
					res = None
					message = "image is too big"
					statusCode = 400

				json_object = json.dumps(originalDataResponce.json())
				with open("response.json", "w") as outfile:
					outfile.write(json_object)

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


@app.route('/imagedb/<string:img_name>',methods=['GET','POST','DELETE','PATCH'])
def addImage(img_name):
	isError = True
	if request.method == 'POST':
		if ("image" in request.files):
			image = Image.open(request.files["image"])
			print(image.format)
			if (image.format == "JPEG"):

				"send the image"
				message = db.sendImage(img_name, image)

				isError = False
				statusCode = 200
			else:
				message = "Request Failed invalid file format"
				statusCode = 400

	if request.method == 'DELETE':
		"delete the image"
		message = db.deleteImage(img_name)
		isError = False
		statusCode = 200

	return jsonify(isError=isError,
				message= message,
				statusCode= statusCode), 200




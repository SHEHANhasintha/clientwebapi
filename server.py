from flask import Flask
from flask import request, jsonify
from PIL import Image
import io

import numpy
import requests
import time
import json
from pprint import pprint

from database.dataBase import Database
from imageRec.imgRec import ImageRec

app = Flask(__name__)

dbLogos = Database("mongodb+srv://logoimage:2XokFEGevhchsP4S@cluster0.hhg7q.mongodb.net/spamdetector?retryWrites=true&w=majority","logonames","spamdetector");
dbCaptures = Database("mongodb+srv://spamcapture:Cx8tmNx7ViuxQJV5@cluster0.hhg7q.mongodb.net/spamcapture?retryWrites=true&w=majority","spamcapture","spamcapture");

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
		if ("image" in request.files ):
			image  = Image.open(request.files["image"])
			print(image.format)
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

				"""url = 'http://ec2-3-86-30-105.compute-1.amazonaws.com/upload'
				files = {'file': open('F:\\work\\projects\profitableProjects\\freelance\\flaskApi_try\\help\\1549549114-New-chairman-appointed-for-BOC-3.jpg','rb')}
				res = requests.post(url, files=files)
				pprint(res.json())"""

				print(originalDataResponce.status_code)
				data = "ok image was taken"

				if (originalDataResponce.status_code == 200):
					message =  "Success logo detection"
					pred = originalDataResponce.json()["predictions"][0]["detection_classes"][0]

					images = dbLogos.getEveryDisp()
					res = 'nomatch'
					count = 1;
					for img in images:
						print(int(count)==int(pred))
						if (int(count) == int(pred)):
							imagePri = Image.open(io.BytesIO(dbLogos.getImage(img['name'])))
							imagePri.save(('received\\' + img['name'] + '.jpg'))
							width, height = imagePri.size
							print(width,height)

							imageReceved = imageOriginal.resize((width, height))
							imageReceved.save("received\\received.jpg")


							ImageR = ImageRec(('received\\' + img['name'] + '.jpg'), "received\\received.jpg");
							#print(ImageR.score())
							if (ImageR.estimate() > 0.1):
								res = {"logoName": img['name'], "proberbility": ImageR.estimate()}
								break;


						count+=1


					isError = False
					statusCode = 200
				else:
					res = None
					message = "image is too big for logo"
					statusCode = 400

				json_object = json.dumps(originalDataResponce.json())
				with open("response.json", "w") as outfile:
					outfile.write(json_object)

			else:
				message = "Request Failed invalid file format for logo"
				res = None
				statusCode = 400
		else:
			isError = True
			statusCode = 400
			res = None
			data = "An image input is required as a logo"

		logoRes = {'isErrorLogo':isError,
				'messageLogo':message,
				'dataLogo':data,
				'reslogo':res,
				'statusCodeLogo':statusCode}



		if request.method == 'POST':
			if ("imagecapture" in request.files):
				image = Image.open(request.files["imagecapture"])
				print(image.format)
				if (image.format == "JPEG"):
					imageOriginal = image
					image.save("received\\receivedCapture.jpg")
					#image = image.resize((10, 10))

					isError = True;
					print("file process is completed")
					#image_np = numpy.array(image)
					payload = {'file': open('F:\\work\\projects\profitableProjects\\freelance\\flaskApi_try\\help\\1549549114-New-chairman-appointed-for-BOC-3.jpg','rb')}
					#start = time.perf_counter()
					originalDataResponce = requests.post('http://ec2-3-86-30-105.compute-1.amazonaws.com/upload', files=payload)



					print(originalDataResponce.json())
					data = "ok image was taken"

					if (originalDataResponce.status_code == 200):
						message = "Success capture detection"
						pred = originalDataResponce.json()[0]["name"]
						res = pred

						images = dbCaptures.getEveryDisp()
						res = 'nomatch'
						count = 1;
						print(images)
						arr = []
						for img in images:
							if (img['name'] == pred):
								imagePri = Image.open(io.BytesIO(dbCaptures.getImage(img['name'])))
								imagePri.save(('received\\' + img['name'] + '_capture.jpg'))
								arr.append(imagePri)
								print(img['name'])

								ImageR = ImageRec(('received\\' + img['name'] + '_capture.jpg'), "received\\receivedCapture.jpg");
								print(ImageR.score())
								res = ImageR.score();


								"""print(int(count) == int(pred))
								if (int(count) == int(pred)):
									imagePri = Image.open(io.BytesIO(dbLogos.getImage(img['name'])))
									imagePri.save(('received\\' + img['name'] + '.jpg'))
									width, height = imagePri.size
									print(width, height)
		
									imageReceved = imageOriginal.resize((width, height))
									imageReceved.save("received\\received.jpg")
		
									ImageR = ImageRec(('received\\' + img['name'] + '.jpg'), "received\\received.jpg");
									# print(ImageR.score())
									if (ImageR.estimate() > 0.1):
										res = {"logoName": img['name'], "proberbility": ImageR.estimate()}
										break;
		
								count += 1"""





						isError = False
						statusCode = 200
					else:
						res = None
						message = "image is too big for logo"
						statusCode = 400

					json_object = json.dumps(originalDataResponce.json())
					with open("response.json", "w") as outfile:
						outfile.write(json_object)

				else:
					message = "Request Failed invalid file format for logo"
					res = None
					statusCode = 400
			else:
				isError = True
				statusCode = 400
				res = None
				data = "An image input is required as a logo"

		captureRes = {'isErrorCapture':isError,
						  'messageCapture':message,
						  'dataCapture':data,
						  'reslogoCapture':res,
						  'statusCodeCapture':statusCode}

		data = {'logopred':logoRes,'capturepred':captureRes}
		return json.dumps(data), 200


@app.route('/imagedb/<string:db>/<string:img_name>',methods=['GET','POST','DELETE','PATCH'])
def addImage(img_name,db):
	isError = True
	statusCode = 400
	if (db == "logos"):
		db = dbLogos

	if (db == "captures"):
		db = dbCaptures
	message = "no effect occured"
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




import PIL.Image
import numpy
import requests
from pprint import pprint
import time
import json

image = PIL.Image.open("paypal.jpg")  # Change with your image
image_np = numpy.array(image)


payload = {"instances": [image_np.tolist()]}
start = time.perf_counter()
res = requests.post("http://ec2-54-196-1-250.compute-1.amazonaws.com/v1/models/default:predict", json=payload)
#print(f"Took {time.perf_counter()-start:.2f}s")
#json_object = json.dumps(res.json())
#with open("hnb.json", "w") as outfile: 
    #outfile.write(json_object) 
#pprint(res.json())

print(res.status_code)

#json_object = json.dumps(res.json())
#with open("response.json", "w") as outfile: 
#    outfile.write(json_object) 

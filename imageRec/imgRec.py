from skimage.metrics import structural_similarity

import cv2

class ImageRec:
	def __init__(self,image1,image2):
		self.image_orig = cv2.imread(image1)
		self.image_mod = cv2.imread(image2)
		self.resized_orig = cv2.resize(self.image_orig, (300, 200))
		self.resized_mod = cv2.resize(self.image_mod, (300, 200))

	def estimate(self):
		# convert the images to grayscale
		gray_orig = cv2.cvtColor(self.resized_orig, cv2.COLOR_BGR2GRAY)
		gray_mod = cv2.cvtColor(self.resized_mod, cv2.COLOR_BGR2GRAY)

		(score, diff) = structural_similarity(gray_orig, gray_mod, full=True)
		diff = (diff * 255).astype("uint8")
		return(score)









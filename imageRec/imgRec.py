from skimage.metrics import structural_similarity

import cv2
import numpy as np

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

	def score(self):
		original = self.image_orig
		image_to_compare = self.image_mod

		# 1) Check if 2 images are equals
		if original.shape == image_to_compare.shape:
			print("The images have same size and channels")
			difference = cv2.subtract(original, image_to_compare)
			b, g, r = cv2.split(difference)

			if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
				print("The images are completely Equal")
			else:
				print("The images are NOT equal")

		# 2) Check for similarities between the 2 images
		sift = cv2.xfeatures2d.SIFT_create()
		kp_1, desc_1 = sift.detectAndCompute(original, None)
		kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

		index_params = dict(algorithm=0, trees=5)
		search_params = dict()
		flann = cv2.FlannBasedMatcher(index_params, search_params)

		matches = flann.knnMatch(desc_1, desc_2, k=2)

		good_points = []
		for m, n in matches:
			if m.distance < 0.6 * n.distance:
				good_points.append(m)

		# Define how similar they are
		number_keypoints = 0
		if len(kp_1) <= len(kp_2):
			number_keypoints = len(kp_1)
		else:
			number_keypoints = len(kp_2)

		print("Keypoints 1ST Image: " + str(len(kp_1)))
		print("Keypoints 2ND Image: " + str(len(kp_2)))
		print("GOOD Matches:", len(good_points))
		print("How good it's the match: ", len(good_points) / number_keypoints * 100)

		result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)

		cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
		# cv2.imwrite("feature_matching.jpg", result)

		#cv2.imshow("Original", cv2.resize(original, None, fx=0.4, fy=0.4))
		#cv2.imshow("Duplicate", cv2.resize(image_to_compare, None, fx=0.4, fy=0.4))
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		data = {'match' : (len(good_points) / number_keypoints * 100), 'comp_window': len(good_points)}

		return data












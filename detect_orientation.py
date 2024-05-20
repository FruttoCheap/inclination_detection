# import the necessary packages
import argparse
from imutils.perspective import four_point_transform
import pytesseract
import cv2
from PIL import Image, ImageEnhance, ImageFilter

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
args = vars(ap.parse_args())

#test1
image = cv2.imread(args["image"])

# Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Convert Gaussian Blur
blur = cv2.GaussianBlur(gray,(5,5),0)

# Convert to Otsu's threshold
otsu,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Use image and threshold to find contours
cnts = cv2.findContours(th2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

for c in cnts:
    # Perform contour approximation
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        displayCnt = approx
        print(displayCnt)
        break

# Obtain birds' eye view of image
warped = four_point_transform(image, displayCnt.reshape(4, 2))

# show the original image and output image after orientation
# correction
cv2.imshow("Original", image)
cv2.imshow("Output", warped)
cv2.waitKey()
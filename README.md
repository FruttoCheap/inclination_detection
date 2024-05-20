# inclination_detection
Simple python script to understand the angle, with respect to the horizontal, of an image of a plate.

# Usage
After activating the venv and install all the needed packages, simply call the file from cli, passing the image path as argument:

python3 detect_orientation.py --image images/P1106V10T20240110144016I01_rear.jpg

To output will be an array of coordinates, indicating where in the image where the 4 original angles of the plate.
import cv2
import numpy as np
import os
import random

def is_similar(image_path1, image_path2, similarity_threshold=0.75):
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Detect keypoints and compute descriptors
    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    # Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(descriptors1, descriptors2)

    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Calculate the average distance of the top matches
    num_top_matches = 30
    average_distance = sum(match.distance for match in matches[:num_top_matches]) / num_top_matches

    # If the average distance is below the threshold, consider the images similar
    return average_distance < similarity_threshold

# Load a list of image file paths from a directory
image_directory = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/cache'
image_files = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith('.jpg') or f.endswith('.png')]

# Choose a random image file
ref_image_path = os.path.join(image_directory, "Kd.png")
print(str(ref_image_path))

# Compare the input image to the random image
input_image_path = os.path.join(image_directory, "Kd.png")
similar = is_similar(input_image_path, ref_image_path)

print(f"Images are {'similar' if similar else 'not similar'}")
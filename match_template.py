from __future__ import print_function
import sys
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

## [global_variables]
use_mask = False
img = None
templ = None
mask = None
image_window = "Source Image"
result_window = "Result window"

match_method = 0
max_Trackbar = 5

input_image_path = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/images/rank_a.png'
input_image_surf = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/cache/Ah.png'

# Resizes a image and maintains aspect ratio
def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the 0idth and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv.resize(image, dim, interpolation=inter)

## [global_variables]
def createMask(img_path, tresh):
    image = cv.imread(img_path)
    # Convert the image to the HSV color space
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
 
    # Define the color range for the mask
    lower_color_range = np.array([0, 0, 0])  # Lower bound (e.g., black)
    upper_color_range = np.array([tresh, tresh, tresh])  # Upper bound (e.g., very dark colors)

    # Create the binary mask
    mask = cv.inRange(hsv_image, lower_color_range, upper_color_range)
    return mask

def convert_to_bw(image):
    # Apply binary thresholding to convert the grayscale image to a black and white image
    _, bw_image = cv.threshold(image, 127, 255, cv.THRESH_BINARY)

    return bw_image

def apply_gaussian_blur(image, kernel_size=5, sigma=0):
    # Apply Gaussian blur to the image using the given kernel size and standard deviation
    blurred_image = cv.GaussianBlur(image, (kernel_size, kernel_size), sigma)

    return blurred_image
def extract_fragment(image, top_left, bottom_right):
    # Extract the fragment of the image defined by the top left and bottom right coordinates
    fragment = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    return fragment

def match_template(template, large_image, mask=None, threshold=0.8):
    # Resize the mask image to match the size of the template image
    if mask is not None:
        mask = cv.resize(mask, (template.shape[1], template.shape[0]))


    # Perform the template matching operation using the mask
    result = cv.matchTemplate(large_image, template, cv.TM_SQDIFF_NORMED, mask=mask)
    plt.imshow(result, cmap='gray')

    # Find the location of the template image within the larger image
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print("min_val: " + str(min_val) + "; max_val" + str(max_val) + "; min loc:" + str(min_loc) + "; max loc:" + str(max_loc))

    # Calculate the similarity percentage of the matched template image
    if max_val >= threshold:
        similarity = round(max_val * 100, 2)
    else:
        similarity = 0

    # Return the similarity percentage and the location of the matched template image
    return similarity, max_loc, result

# Load the template and larger image
template = cv.imread(input_image_path, 0)
large_image = cv.imread(input_image_surf, 0)

# Load the mask image
mask = createMask(input_image_path, 150)
cv.imshow('mask', mask)

# Resize the mask image to match the size of the template image
mask = cv.resize(mask, (template.shape[1], template.shape[0]))

# Find the similarity percentage and location of the matched template image
similarity, location, result = match_template(template, large_image, mask=mask)
treshold = 0.9
loc = np.where( result >= treshold)
print("similarity: " + str(similarity) + "%")

# Draw a rectangle around the matched region in the larger image
if similarity > 0:
    template_height, template_width = template.shape[:2]
    top_left = location
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)   
    for pt in zip(*loc[::-1]):
        cv.rectangle(large_image, top_left, bottom_right, (0, 255, 255), 2)
        cv.imshow('Matched Image', large_image)

# Display the matched image and similarity percentage



cv.waitKey(0)
cv.destroyAllWindows()
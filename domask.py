import cv2
import numpy as np

# Load the input image
input_image_path = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/images/suit_club_base.png'
input_image_surf = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/cache/Tc.png'

image = cv2.imread(input_image_path)
image_s = cv2.imread(input_image_surf)

# Convert the image to the HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hsv_image_s = cv2.cvtColor(image_s, cv2.COLOR_BGR2HSV)

# Define the color range for the mask
lower_color_range = np.array([0, 0, 0])  # Lower bound (e.g., black)
upper_color_range = np.array([100, 100, 100])  # Upper bound (e.g., very dark colors)

# Create the binary mask
mask = cv2.inRange(hsv_image, lower_color_range, upper_color_range)
mask_s = cv2.inRange(hsv_image_s, lower_color_range, upper_color_range)

#method_accepts_mask = (cv2.TM_SQDIFF == match_method or match_method == cv.TM_CCORR_NORMED)
img = cv2.cvtColor(image_s, cv2.COLOR_BGR2GRAY)
templ = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

result = cv2.matchTemplate(img, templ, cv2.TM_CCORR_NORMED, None, mask)

cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )    
_minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
matchLoc = maxLoc

cv2.rectangle(image_s, matchLoc, (matchLoc[0] + templ.shape[0], matchLoc[1] + templ.shape[1]), (0,0,0), 2, 8, 0 )
cv2.rectangle(result, matchLoc, (matchLoc[0] + templ.shape[0], matchLoc[1] + templ.shape[1]), (0,0,0), 2, 8, 0 )
#cv2.imshow(image_window, img_display)
#cv2.imshow(image_s, result)

# Display the original image and the mask side by side
cv2.imshow('Original Image', image)
cv2.imshow('Mask Image', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
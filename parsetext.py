import cv2
import pytesseract

def read_and_print(input_file):
    # Load the image
    image = cv2.imread(input_file)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to binarize the image
    threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    # Use Tesseract OCR to extract the text
    text = pytesseract.image_to_string(threshold)
    # Split the text into individual lines
    lines = text.split('\n')
    # Filter out empty lines
    lines = [line for line in lines if line.strip() != '']
    # Print the list of text labels
    print(lines)

input_file = "C:/Users/plus3/OneDrive/Desktop/cards/default/1440/textimg/cashier.png"
read_and_print(input_file)
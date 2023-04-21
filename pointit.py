import pyautogui
import pygetwindow as gw
from PIL import Image, ImageDraw, ImageFont
import time

def find_window_by_position(x, y):
    for window in gw.getAllWindows():
        if window.left <= x <= window.left + window.width and window.top <= y <= window.top + window.height:
            return window
    return None

# Wait for user to click on a window
print("Click on the window you want to capture. You have 5 seconds.")
time.sleep(5)
x, y = pyautogui.position()

# Find the clicked window
target_window = find_window_by_position(x, y)

if target_window is not None:
    # Take a screenshot of the window
    screenshot = pyautogui.screenshot(region=(target_window.left, target_window.top, target_window.width, target_window.height))

    # Add width and height information to the screenshot
    draw = ImageDraw.Draw(screenshot)
    font = ImageFont.truetype("arial.ttf", 16)
    text = f"{target_window.width}x{target_window.height}"
    text_width, text_height = draw.textsize(text, font=font)
    draw.text((target_window.width - text_width - 5, target_window.height - text_height - 5), text, font=font, fill=(0, 0, 0))

    # Show the screenshot
    screenshot.show()
else:
    print("Window not found.")
import pygetwindow as gw
from PIL import ImageGrab
from pywinauto import Application
import sys
import time

def get_window_by_title_substring(substring):
    windows = gw.getAllTitles()
    for window_title in windows:
        if substring in window_title:
            return gw.getWindowsWithTitle(window_title)[0]
    return None

def is_window_visible(app_window):
    return app_window.is_visible()

def bring_window_to_front(app_window):
    if not app_window.is_visible():
        app_window.set_focus()
        app_window.set_foreground()

def take_window_screenshot(window, save_as="C:/Users/plus3/OneDrive/Desktop/cards/default/1440/textimg/screenshot.png"):
    left, top, width, height = window.left, window.top, window.width, window.height
    screenshot = ImageGrab.grab(bbox=(left, top, left+width, top+height), include_layered_windows=True, all_screens=True)
    screenshot.save(save_as)

window_title_substring = 'PokerStars'
window = get_window_by_title_substring(window_title_substring)

if window:
    app = Application().connect(handle=window._hWnd)
    app_window = app.window(handle=window._hWnd)
    if app_window.is_minimized():
        app_window.restore()
        bring_window_to_front(app_window)
        time.sleep(0.1)  # Give the window time to restore before taking a screenshot
        take_window_screenshot(window)
        app_window.minimize()
    else:
        app_window.minimize()
        app_window.restore()
        bring_window_to_front(app_window)
        time.sleep(0.1)  # Give the window time to restore before taking a screenshot
        take_window_screenshot(window)

if window:
    take_window_screenshot(window)
    print(f"Screenshot of the window containing '{window_title_substring}' saved as 'screenshot.png'.")
else:
    print(f"No window found with title containing '{window_title_substring}'.")
    sys.exit(-1)
import os
import time
import psutil
import win32gui
import win32process
import win32ui
import win32con
from PIL import ImageGrab
from pynput import keyboard

# Directory where screenshots will be saved
save_directory = r".\\screenshots"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Screenshot counter
screenshot_counter = 1

# Function to get the window rectangle by process name
def get_window_rect_by_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            pid = proc.info['pid']
            break
    else:
        print(f"Process '{process_name}' not found!")
        return None

    def callback(hwnd, pid):
        if win32gui.IsWindowVisible(hwnd):
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                rect = win32gui.GetWindowRect(hwnd)
                return rect  # Return the rectangle directly
        return None

    windows = []
    win32gui.EnumWindows(lambda hwnd, result_list: result_list.append(callback(hwnd, pid)), windows)
    windows = [win for win in windows if win is not None]

    if windows:
        return windows[0]
    else:
        print(f"No windows found for process '{process_name}'!")
        return None

def on_press(key):
    global screenshot_counter
    global window_rect

    try:
        if key.char == 'c':  # Replace 'c' with the key of your choice
            if window_rect is not None:
                screenshot = ImageGrab.grab(bbox=window_rect)  # Capture only the specified window
                screenshot_path = os.path.join(save_directory, f"screenshot_{screenshot_counter}.png")
                screenshot.save(screenshot_path)
                print(f"Screenshot {screenshot_counter} saved to {screenshot_path}")
                screenshot_counter += 1
            else:
                print("Window not found. No screenshot taken.")
    except AttributeError:
        pass

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    process_name = "ac_client.exe"  # Replace with your game's process name
    window_rect = get_window_rect_by_process(process_name)

    if window_rect is not None:
        print("Press 'c' to take a screenshot.")
        print(f"Screenshots will be saved in {save_directory}")
        start_listener()
    else:
        print("Could not find the game window.")

import cv2
import mss
import numpy as np
import psutil
import win32gui
import win32process
from ultralytics import YOLO

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
                return {"top": rect[1], "left": rect[0], "width": rect[2] - rect[0], "height": rect[3] - rect[1]}
        return None

    windows = []
    win32gui.EnumWindows(lambda hwnd, result_list: result_list.append(callback(hwnd, pid)), windows)
    windows = [win for win in windows if win is not None]

    if windows:
        return windows[0]
    else:
        print(f"No windows found for process '{process_name}'!")
        return None

# Replace 'ac_client.exe' with your game process name
monitor = get_window_rect_by_process('ac_client.exe')

if monitor:
    model = YOLO(r".\assaultcube_trained_model\best.pt")

    with mss.mss() as sct:
        while True:
            # Capture the game window
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format for OpenCV

            # Run YOLO model on the captured image
            results = model(img)

            # Draw the results on the frame
            result_img = results[0].plot()

            # Display the frame with detections
            cv2.imshow("Game Window - YOLO Detection", result_img)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
else:
    print("Could not find the game window.")

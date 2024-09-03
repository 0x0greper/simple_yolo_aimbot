import cv2
import numpy as np
import psutil
import win32gui
import win32process
import win32api
import mss
from pynput import keyboard
from ultralytics import YOLO
import threading

# Load the pretrained YOLOv8 model
model = YOLO(r".\assaultcube_trained_model\best.pt")
model.to("cuda")  # Ensure YOLO is using GPU

# Global variables to store the last detection results
last_results = None
last_window_position = None

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

# Function to draw bounding boxes
def draw_boxes(image, detections):
    for detection in detections:
        cls = int(detection.cls[0])
        if cls in [0, 1]:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            color = (0, 255, 0) if cls == 0 else (0, 0, 255)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            label = "bad_guy_body" if cls == 0 else "bad_guy_head"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

# Function to move the mouse to the center of the detected bad_guy_head
def move_mouse_to_target(detections, window_position):
    for detection in detections:
        cls = int(detection.cls[0])
        if cls == 1:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            center_x = (x1 + x2) // 2 + window_position["left"]
            center_y = (y1 + y2) // 2 + window_position["top"]
            win32api.SetCursorPos((center_x, center_y))
            break

# Function to capture the "q" key press
def on_press(key):
    try:
        if key.char == 'q':
            if last_results is not None and last_window_position is not None:
                move_mouse_to_target(last_results[0].boxes, last_window_position)
    except AttributeError:
        pass

def listen_to_keyboard():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    process_name = "ac_client.exe"  # Replace with your game process name

    monitor = get_window_rect_by_process(process_name)
    if monitor:
        cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)

        # Start keyboard listener in a separate thread
        threading.Thread(target=listen_to_keyboard, daemon=True).start()

        with mss.mss() as sct:
            while True:
                frame = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                results = model(frame)

                last_results = results
                last_window_position = monitor

                draw_boxes(frame, results[0].boxes)

                cv2.imshow('Detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()
    else:
        print("Could not find the game window.")

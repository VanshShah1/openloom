
import tkinter as tk
import pyautogui
import cv2
import numpy as np
import threading
import time
from PIL import Image, ImageTk

class LoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenLoom")
        self.root.geometry("150x50+100+100")
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.8)
        self.root.attributes("-topmost", True)

        self.is_recording = False
        self.recording_thread = None

        self.record_button = tk.Button(self.root, text="Record", command=self.toggle_recording)
        self.record_button.pack(pady=10)

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.record_button.config(text="Recording...")
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(text="Record")

    def record_screen(self):
        for i in range(3, 0, -1):
            self.record_button.config(text=str(i))
            time.sleep(1)
        
        self.record_button.config(text="Stop")

        # Capture first screenshot to get accurate screen dimensions
        first_screenshot = pyautogui.screenshot()
        screen_width, screen_height = first_screenshot.size

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter("output.mp4", fourcc, 30.0, (screen_width, screen_height))

        print(f"Screen size: {screen_width}x{screen_height}")

        if not out.isOpened():
            print("Error: Could not open video writer.")
            return

        print(f"Screen size: {screen_width}x{screen_height}")

        while self.is_recording:
            start_time = time.time()
            img = pyautogui.screenshot()
            frame = np.array(img)
            # Convert RGB to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)

            end_time = time.time()
            elapsed_time = end_time - start_time
            # Target FPS is 30, so each frame should take 0.0333 seconds
            if elapsed_time < 0.0333:
                time.sleep(0.0333 - elapsed_time)
            
            # Calculate and print actual FPS
            actual_fps = 1 / (time.time() - start_time)
            print(f"Actual FPS: {actual_fps:.2f}")
            
            # Calculate and print actual FPS
            actual_fps = 1 / (time.time() - start_time)
            print(f"Actual FPS: {actual_fps:.2f}")

        out.release()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoomApp(root)
    root.mainloop()

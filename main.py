import pyautogui
import cv2
import numpy as np
import time
import os

# Define screen dimensions
screen_width, screen_height = pyautogui.size()

# Define the duration of the recording in seconds
record_duration = 10

# Define the frames per second for the output video
fps = 20.0

# Define the codec and create VideoWriter object
# You can try 'XVID' or 'mp4v' depending on what codecs are available on your system
# For macOS, 'mp4v' is usually a good choice for MP4 files
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Determine the path to the desktop
# This part might need adjustment based on your operating system
# For macOS, it's typically /Users/YourUsername/Desktop
# For Windows, it's typically C:\\Users\\YourUsername\\Desktop
# For Linux, it can vary, often /home/YourUsername/Desktop
# Replace 'YourUsername' with your actual username or make this dynamic
# A more robust way might be to use os.path.expanduser("~/Desktop")
# Given your workspace path is /Users/vanshshah/Documents/GitHub/openloom,
# your desktop is likely /Users/vanshshah/Desktop
desktop_path = os.path.expanduser("~/Desktop") # This is generally cross-platform

# Define the output file name and path
output_filename = os.path.join(desktop_path, 'screen_recording.mp4')

out = cv2.VideoWriter(output_filename, fourcc, fps, (screen_width, screen_height))

# Calculate the number of frames to capture
num_frames = int(record_duration * fps)

try:
    print(f"Starting screen recording for {record_duration} seconds...")

    start_time = time.time()

    for i in range(num_frames):
        # Capture screenshot
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert RGB to BGR (OpenCV uses BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the video file
        out.write(frame)

        # Optional: Add a small delay to try and match the desired frame rate
        # This is a simple approach and might not be perfectly accurate
        time.sleep(1/fps)

        # Check if duration has passed (alternative way to stop)
        if time.time() - start_time > record_duration:
            break

    print(f"Recording finished. Saving video to {output_filename}")
finally:
    # Release the video writer object
    out.release()
    print("Video writer released.")

print("Video saved successfully!")
import pyautogui
import cv2
import numpy as np
import time
import os

# --- CONFIGURATION ---
# Define the duration of the recording in seconds
record_duration = 100
# Define the frames per second for the output video
fps = 20.0
# Define the codec. 'mp4v' is a good choice for .mp4 files on macOS and Linux.
# You could also try 'avc1'. For .avi files, 'XVID' is common on Windows.
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# --- SETUP OUTPUT PATH ---
# Get the path to the user's desktop in a cross-platform way
desktop_path = os.path.expanduser("~/Desktop")
# Define the output file name and full path
output_filename = os.path.join(desktop_path, 'screen_recording.mp4')

# --- BUG FIX: DYNAMICALLY GET SCREEN SIZE ---
# Take a sample screenshot to determine the correct screen dimensions.
# This is the most reliable way to avoid size mismatches, especially on
# HiDPI/Retina displays where scaling can cause issues.
print("Determining screen dimensions...")
initial_screenshot = pyautogui.screenshot()
screen_width, screen_height = initial_screenshot.size
print(f"Screen dimensions detected: {screen_width}x{screen_height}")

# --- INITIALIZE VIDEO WRITER ---
# Create the VideoWriter object with the guaranteed correct dimensions
out = cv2.VideoWriter(output_filename, fourcc, fps, (screen_width, screen_height))

# Check if the VideoWriter was initialized successfully
if not out.isOpened():
    print("Error: Could not open video writer.")
    print("Please check the specified codec, output file path, and permissions.")
    exit()

# --- RECORDING LOOP ---
print(f"Starting screen recording for {record_duration} seconds...")
print(f"Output will be saved to: {output_filename}")

start_time = time.time()

try:
    # This loop will run for the specified duration
    while (time.time() - start_time) < record_duration:
        # --- FIX: Synchronize capture rate with FPS ---
        # Record the start time of this loop iteration.
        loop_start_time = time.time()

        # Capture a screenshot
        img = pyautogui.screenshot()

        # Convert the screenshot (PIL Image) to a numpy array
        frame = np.array(img)

        # Convert the color space from RGB (used by pyautogui) to BGR (used by OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the BGR frame to the video file
        out.write(frame)

        # --- FIX: Calculate time to wait to maintain FPS ---
        # Calculate how long the frame capture and processing took.
        time_elapsed = time.time() - loop_start_time
        # Calculate the required sleep time to hit the target FPS.
        # For example, if FPS is 20, each frame should take 1/20 = 0.05 seconds.
        # If processing took 0.02s, we sleep for the remaining 0.03s.
        sleep_for = (1.0 / fps) - time_elapsed
        if sleep_for > 0:
            time.sleep(sleep_for)

    print("Recording finished.")

finally:
    # --- CLEANUP ---
    # Always release the video writer to finalize the video file.
    # This is crucial for preventing file corruption.
    out.release()
    print("Video writer released. File has been saved.")

print("Process complete!")

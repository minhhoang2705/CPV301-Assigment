import cv2
import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()


def use_camera():
    # Open the video capture device (in this case, the default webcam)
    cap = cv2.VideoCapture(0)

    # Set the frame size (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Initialize a frame counter
    frame_num = 0

    while True:
        # Read a frame from the video capture device
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            break

        # Crop the frame to a region of interest (ROI)
        # In this example, we crop the top-left quarter of the frame
        height, width, _ = frame.shape
        roi = frame[0:height//2, 0:width//2]

        # Save the cropped frame as an image file
        filename = f'frame_{frame_num:04d}.png'
        cv2.imwrite(filename, roi)

        # Increment the frame counter
        frame_num += 1

        # Display the original frame with the ROI overlaid
        cv2.rectangle(frame, (0, 0), (width//2, height//2), (0, 255, 0), 2)
        cv2.imshow('frame', frame)

        # Wait for a key press and check if the 'q' key was pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close the window
    cap.release()
    cv2.destroyAllWindows()


# Size and title of the app
window.geometry("1200x1000")
window.title("Assignment")

# Create button to interact
b1 = tk.Button(window, text='Use Camera', width=20,
               command=lambda: use_camera())

# Show the button
b1.grid(row=2, column=1)


window.mainloop()

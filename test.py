import cv2
import tkinter as tk

class App:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.root = tk.Tk()
        self.root.title("Video Cropper")

# Creating a canvas with the width and height of the video frame.
        self.canvas = tk.Canvas(self.root, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.rect = None
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.root.bind("<Escape>", lambda event: self.root.quit())

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        # Get the current frame
        ret, frame = self.cap.read()

        # Get the coordinates of the rectangle
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # Crop the frame to the region of interest
        cropped_frame = frame[int(y1):int(y2), int(x1):int(x2)]

        # Save the cropped frame as an image file
        cv2.imwrite("cropped_frame.png", cropped_frame)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.canvas.create_image(0, 0, anchor=tk.NW, image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.root.update()

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = App()
    app.run()

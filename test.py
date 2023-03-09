import cv2
import tkinter as tk
from PIL import Image, ImageTk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Video Cropper")
        self.video_capture = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(self.root, width=self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.crop_button = tk.Button(
            self.root, text="Crop", command=self.crop_video)
        self.crop_button.pack()
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.root.bind("<Button-1>", self.start_crop)
        self.root.bind("<ButtonRelease-1>", self.stop_crop)
        self.root.bind("<B1-Motion>", self.draw_crop_rect)
        self.current_frame = None
        self.update()

    def update(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.current_frame = frame  # update current frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.root.after(15, self.update)

    def start_crop(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def stop_crop(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

    def draw_crop_rect(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x,
                           self.start_y, self.end_x, self.end_y)

    def crop_video(self):
        if self.start_x is None or self.start_y is None or self.end_x is None or self.end_y is None:
            # If the crop values have not been set, do nothing
            return

        # Crop the current frame using the selected region
        cropped_frame = self.current_frame[int(self.start_y):int(self.end_y),
                                           int(self.start_x):int(self.end_x), :]

        # Save the cropped frame as an image file
        if cropped_frame.size > 0:
            cv2.imwrite("cropped_frame.jpg", cropped_frame)
            print("Saved cropped frame as 'cropped_frame.jpg'")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

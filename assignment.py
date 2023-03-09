import cv2
import tkinter as tk
from tkinter import *

window = tk.Tk()

def use_camera(my_window):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        cv2.imshow('Frame', frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

b1 = tk.Button(window, text= 'Use Camera', command=lambda: use_camera(window))
b1.pack()
window.title("Assignment")
window.geometry("1080x920")

window.mainloop()
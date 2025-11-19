# C:\Users\shagu\Python\ObjectDetection\detect_gui.py
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from detection.detect_model import load_model
from detection.detect_core import analyze_image

MODEL_PATH = r"C:\Users\shagu\Python\ObjectDetection\models\best.pt"
model = load_model(MODEL_PATH)

def open_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if not path:
        return

    img, detections = analyze_image(model, path)

    for d in detections:
        x1, y1, x2, y2 = d["box"]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

    cv2.imshow("Detection Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

root = tk.Tk()
root.title("Cube Detector GUI")

btn = tk.Button(root, text="画像を選択して検出", command=open_image, width=30, height=2)
btn.pack(pady=20)

root.mainloop()

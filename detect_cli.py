# detect_cli.py
import os
import cv2
import csv
from detection.detect_model import load_model
from detection.detect_core import analyze_image

MODEL_PATH = r"C:\Users\shagu\Python\ObjectDetection\models\cube_yolov8n\weights\best.pt"

INPUT_FOLDER = r"C:\Users\shagu\Python\ObjectDetection\input_images"
OUTPUT_FOLDER = r"C:\Users\shagu\Python\ObjectDetection\output_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

CSV_PATH = os.path.join(OUTPUT_FOLDER, "results.csv")

model = load_model(MODEL_PATH)

with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "score", "distance_cm", "brightness", "angle"])

    for file in os.listdir(INPUT_FOLDER):
        if not file.lower().endswith((".png", ".jpg")):
            continue

        path = os.path.join(INPUT_FOLDER, file)
        img, detections = analyze_image(model, path)

        for d in detections:
            x1, y1, x2, y2 = d["box"]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

            writer.writerow([file, d["score"], d["distance_cm"], d["brightness"], d["angle"]])

        cv2.imwrite(os.path.join(OUTPUT_FOLDER, file), img)

print("✅ 一括検出完了: 結果 →", OUTPUT_FOLDER)

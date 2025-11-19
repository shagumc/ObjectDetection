# detection/detect_model.py
import torch
from ultralytics import YOLO


def load_model(model_path):
    print(f"[INFO] Loading YOLO model: {model_path}")
    model = YOLO(model_path)
    return model


def detect_objects(model, image_path, conf=0.25):
    """GPU が使えない場合は自動で CPU に変更"""
    if torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    print(f"[INFO] Using device: {device}")

    results = model.predict(
        source=image_path,
        conf=conf,
        device=device,
        save=False
    )
    return results

# detection/detect_core_basic.py
import cv2
from detection.detect_model import detect_objects

def analyze_image_basic(model, image_path):
    """
    YOLO の検出結果をそのまま描画する一般用検出関数。
    白いキューブに限定しない。
    """
    img = cv2.imread(image_path)
    if img is None:
        return None, []

    results = detect_objects(model, image_path)
    detections = []

    for r in results:
        names = r.names  # モデルに登録されているクラス名一覧

        for box in r.boxes:
            cls_id = int(box.cls[0])
            class_name = names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                "box": (x1, y1, x2, y2),
                "class_id": cls_id,
                "class_name": class_name,
                "conf": conf
            })

            # 描画処理
            label = f"{class_name} ({conf:.2f})"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 200, 0), 2)
            cv2.putText(img, label, (x1, y1 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)

    return img, detections

# gui/detect_gui_basic.py
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import sys
import os

# パス設定
BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, ".."))
sys.path.append(PROJECT_ROOT)

# 検出コア
from detection.detect_model import load_model
from detection.detect_core_basic import analyze_image_basic

# モデルパス
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "best.pt")

# ----------------------------------------------
#  YOLO モデル読み込み
# ----------------------------------------------
if not os.path.exists(MODEL_PATH):
    messagebox.showerror("エラー", f"best.pt がありません:\n{MODEL_PATH}")
    raise SystemExit

print(f"[INFO] Loading YOLO model: {MODEL_PATH}")
model = load_model(MODEL_PATH)

# ----------------------------------------------
#  GUI イベント
# ----------------------------------------------
def detect_image():
    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.png *.jpeg")]
    )
    if not path:
        return

    img, dets = analyze_image_basic(model, path)

    if img is None:
        messagebox.showerror("エラー", "画像を読み込めませんでした。")
        return

    # 検出結果をコンソールへ
    print(f"=== Detection Result ===")
    for d in dets:
        print(f"- {d['class_name']}  conf={d['conf']:.2f}  box={d['box']}")

    # OpenCVで表示
    cv2.imshow("YOLO Detection Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ----------------------------------------------
#  GUI本体
# ----------------------------------------------
root = tk.Tk()
root.title("YOLO Object Detector (汎用検出GUI)")
root.geometry("430x180")

label = tk.Label(root, text="YOLO 検出（一般物体検出）", font=("Meiryo", 18, "bold"))
label.pack(pady=15)

btn = tk.Button(
    root,
    text="画像を選択して検出する",
    width=30,
    height=2,
    font=("Meiryo", 12),
    command=detect_image,
)
btn.pack(pady=10)

root.mainloop()

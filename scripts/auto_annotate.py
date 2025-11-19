"""
auto_annotate.py
-------------------------------------
GUIで指定された train / val / test 各フォルダを対象に、
学習済みモデル (best.pt) を使用して自動アノテーション (.txt) を生成します。
既存の labels フォルダがある場合は削除して再生成します。
"""

import os
import sys
import shutil
from ultralytics import YOLO
from tkinter import messagebox

# ==============================================================
# 1. GUIから環境変数で渡されたパスを取得
# ==============================================================
TRAIN_DIR = os.getenv("TRAIN_DIR", "./data/train")
VAL_DIR = os.getenv("VAL_DIR", "./data/val")
TEST_DIR = os.getenv("TEST_DIR", "./data/test")
MODEL_PATH = os.getenv("BEST_MODEL", "./models/best.pt")

TARGET_DIRS = {
    "train": os.path.join(TRAIN_DIR, "images"),
    "val": os.path.join(VAL_DIR, "images"),
    "test": os.path.join(TEST_DIR, "images")
}

# ==============================================================
# 2. モデル読み込み
# ==============================================================
if not os.path.exists(MODEL_PATH):
    messagebox.showerror("エラー", f"モデルファイルが見つかりません:\n{MODEL_PATH}")
    sys.exit(1)

model = YOLO(MODEL_PATH)

# ==============================================================
# 3. 各フォルダを処理
# ==============================================================
for name, image_dir in TARGET_DIRS.items():
    if not os.path.exists(image_dir):
        continue

    # 出力先 labels フォルダを設定
    label_dir = image_dir.replace("images", "labels")

    # --- 既存フォルダがあれば削除して再作成 ---
    if os.path.exists(label_dir):
        try:
            shutil.rmtree(label_dir)
            print(f"既存フォルダを削除しました: {label_dir}")
        except Exception as e:
            messagebox.showerror("削除エラー", f"{label_dir} の削除に失敗しました:\n{e}")
            continue
    os.makedirs(label_dir, exist_ok=True)

    # --- 画像ファイル一覧 ---
    image_files = [f for f in os.listdir(image_dir)
                   if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    print(f"\n=== {name.upper()} セットの自動アノテーションを開始 ===")

    for i, filename in enumerate(image_files, 1):
        img_path = os.path.join(image_dir, filename)
        results = model(img_path)

        for r in results:
            h, w = r.orig_shape
            txt_path = os.path.join(label_dir, filename.rsplit(".", 1)[0] + ".txt")

            with open(txt_path, "w", encoding="utf-8") as f:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = map(float, box.xyxy[0])

                    # YOLOフォーマット (class cx cy w h)
                    cx = ((x1 + x2) / 2) / w
                    cy = ((y1 + y2) / 2) / h
                    bw = (x2 - x1) / w
                    bh = (y2 - y1) / h

                    f.write(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")

        print(f"[{i}/{len(image_files)}] {filename} → {label_dir}")

# ==============================================================
# 4. classes.txt を自動生成
# ==============================================================
# train/val/test のいずれかに書き込む（同一内容）
def create_classes_txt(base_path):
    labels_path = os.path.join(base_path, "labels")
    if os.path.exists(labels_path):
        classes_file = os.path.join(labels_path, "classes.txt")
        with open(classes_file, "w", encoding="utf-8") as f:
            f.write("cube\n")  # クラス名は1行1つ
        print(f"classes.txt を作成しました: {classes_file}")

# train / val / test それぞれに作成
for p in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    create_classes_txt(p)

# ==============================================================
# 5. 完了ダイアログ表示
# ==============================================================
messagebox.showinfo(
    "完了",
    "train / val / test 各フォルダの自動アノテーションが完了しました。\n"
    "既存の labels フォルダは削除され、再生成されています。"
)

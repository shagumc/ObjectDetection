# scripts\split_train_val_test.py
import os, random, shutil
from tkinter import messagebox
import sys

# GUIから環境変数で受け取る
data_dir = os.getenv("DATA_DIR", "./trainingData")
train_dir = os.getenv("TRAIN_DIR", "./data/train")
val_dir = os.getenv("VAL_DIR", "./data/val")
test_dir = os.getenv("TEST_DIR", "./data/test")

SPLIT_RATIOS = {"train": 0.7, "val": 0.2, "test": 0.1}

if not os.path.exists(data_dir):
    messagebox.showerror("エラー", f"指定されたフォルダが存在しません:\n{data_dir}")
    sys.exit(1)

files = [f for f in os.listdir(data_dir) if f.lower().endswith((".jpg", ".png"))]
if not files:
    messagebox.showerror("エラー", "画像ファイルが見つかりません。")
    sys.exit(1)

random.shuffle(files)

n_train = int(len(files) * SPLIT_RATIOS["train"])
n_val = int(len(files) * SPLIT_RATIOS["val"])

splits = {
    "train": files[:n_train],
    "val": files[n_train:n_train + n_val],
    "test": files[n_train + n_val:]
}

for split_name, file_list in splits.items():
    if split_name == "train":
        target_base = train_dir
    elif split_name == "val":
        target_base = val_dir
    else:
        target_base = test_dir

    img_dir = os.path.join(target_base, "images")
    label_dir = os.path.join(target_base, "labels")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    for f in file_list:
        shutil.copy2(os.path.join(data_dir, f), os.path.join(img_dir, f))
        txt = f.rsplit('.', 1)[0] + ".txt"
        src_txt = os.path.join(data_dir, txt)
        if os.path.exists(src_txt):
            shutil.copy2(src_txt, os.path.join(label_dir, txt))

messagebox.showinfo(
    "完了",
    f"データ振り分けが完了しました。\n\n"
    f"train: {train_dir}\nval: {val_dir}\ntest: {test_dir}"
)

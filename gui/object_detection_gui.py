# gui/object_detection_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import sys

# ---- 学習パラメータ設定ダイアログ ----
from train_dialog import TrainDialog


# ==========================================================
# ★ BASE パス定義
#    このファイルは /ObjectDetection/gui/ 配下に存在
# ==========================================================
GUI_BASE = os.path.dirname(os.path.abspath(__file__))      # /gui
BASE = os.path.dirname(GUI_BASE)                           # /ObjectDetection


# ==========================================================
# ★ デフォルトパス設定
# ==========================================================
DEFAULTS = {
    "data_dir": os.path.join(BASE, "trainingData"),
    "train_dir": os.path.join(BASE, "data", "train"),
    "val_dir": os.path.join(BASE, "data", "val"),
    "test_dir": os.path.join(BASE, "data", "test"),
    "models_dir": os.path.join(BASE, "models"),
    "best_model": os.path.join(BASE, "models", "best.pt"),
}


# ==========================================================
# ★ 共通スクリプト実行
# ==========================================================
def run_script(rel_path, extra_env=None):
    script_path = os.path.join(BASE, rel_path)
    script_path = os.path.abspath(script_path)

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    print(f"▶ RUN: {script_path}")
    subprocess.Popen([sys.executable, script_path], env=env)


# ==========================================================
# ★ 各ボタンの処理関数
# ==========================================================
def run_split_dataset():
    run_script(os.path.join("scripts", "split_train_val_test.py"), collect_env())


def run_labelimg():
    try:
        subprocess.Popen(["labelImg"])
    except Exception:
        messagebox.showerror(
            "Error",
            "LabelImg を起動できませんでした。\n"
            "仮想環境が有効か確認してください。\n"
            "pip install labelImg"
        )


def run_train_dialog():
    """★ 学習パラメータ設定ダイアログを開く"""
    TrainDialog(root, collect_env())

def run_auto_annotation():
    run_script(os.path.join("scripts", "auto_annotate.py"), collect_env())


def run_detector():
    run_script(os.path.join("gui", "detect_test_gui.py"), collect_env())


# ==========================================================
# ★ GUI構築
# ==========================================================
root = tk.Tk()
root.title("Object Detection Manager（検出モデル作成・確認ツール）")
root.geometry("820x950")

title = tk.Label(root, text="Object Detection Manager", font=("Meiryo", 22, "bold"))
title.pack(pady=10)


# ==========================================================
# ★ パス設定エリア
# ==========================================================
frame_paths = tk.LabelFrame(root, text="パス設定（必要に応じて変更可）", font=("Meiryo", 12, "bold"))
frame_paths.pack(padx=10, pady=6, fill="x")

entries = {}


def choose_dir(key):
    """フォルダ選択"""
    path = filedialog.askdirectory(title=f"{key} を選択")
    if path:
        entries[key].delete(0, tk.END)
        entries[key].insert(0, path)


def choose_file(key):
    """best.pt 用ファイル選択"""
    path = filedialog.askopenfilename(title=f"{key} を選択", filetypes=[("PyTorch Model", "*.pt")])
    if path:
        entries[key].delete(0, tk.END)
        entries[key].insert(0, path)


def open_folder(path):
    """フォルダを開く"""
    if not os.path.exists(path):
        messagebox.showerror("エラー", f"パスが存在しません:\n{path}")
        return
    os.startfile(path)


# 行生成
for label, key in [
    ("学習元フォルダ", "data_dir"),
    ("train 出力先", "train_dir"),
    ("val 出力先", "val_dir"),
    ("test 出力先", "test_dir"),
    ("モデル保存フォルダ", "models_dir"),
    ("使用モデル (best.pt)", "best_model"),
]:
    frm = tk.Frame(frame_paths)
    frm.pack(fill="x", pady=3)

    tk.Label(frm, text=f"{label}:", width=20, anchor="w").pack(side="left")

    ent = tk.Entry(frm, width=60)
    ent.insert(0, DEFAULTS[key])
    ent.pack(side="left", padx=4)
    entries[key] = ent

    # 参照ボタン（フォルダ or pt）
    if key == "best_model":
        tk.Button(frm, text="参照", command=lambda k=key: choose_file(k)).pack(side="left", padx=2)
    else:
        tk.Button(frm, text="参照", command=lambda k=key: choose_dir(k)).pack(side="left", padx=2)

    # フォルダを開く
    tk.Button(frm, text="開く", command=lambda k=key: open_folder(entries[k].get())).pack(side="left", padx=2)


# ---- Entry の値を環境変数にして返す ----
def collect_env():
    return {k.upper(): e.get() for k, e in entries.items()}


# ==========================================================
# ★ 説明文
# ==========================================================
desc = (
"【このアプリについて】\n"
"・物体検出モデル（YOLO）を作成するためのワークフローを管理します。\n\n"
"【初回学習】\n"
"1. 画像を train/val/test に分割\n"
"2. LabelImg で手動アノテーション\n"
"3. 学習パラメータを設定し、train.py で学習 → best.pt を生成\n\n"
"【精度向上（2回目以降）】\n"
"・best.pt で自動アノテーション → LabelImg で修正 → 再学習\n\n"
"【確認アプリ】\n"
"・生成した best.pt を使い、画像検出結果を GUI で確認できます。\n"
)
txt = scrolledtext.ScrolledText(root, width=95, height=12, wrap=tk.WORD)
txt.insert(tk.END, desc)
txt.config(state=tk.DISABLED)
txt.pack(pady=10)


# ==========================================================
# ★ ボタン群
# ==========================================================
tk.Button(root, text="① train / val / test に分割", width=70, command=run_split_dataset).pack(pady=4)

tk.Label(root, text="【初回学習フロー】", font=("Meiryo", 14, "bold")).pack(pady=6)
tk.Button(root, text="② LabelImg で手動アノテーション", width=70, command=run_labelimg).pack(pady=4)
tk.Button(root, text="③ 学習開始（詳細設定ダイアログ）", width=70, bg="#ffdddd",
          command=run_train_dialog).pack(pady=10)

tk.Label(root, text="【2回目以降の精度向上】", font=("Meiryo", 14, "bold")).pack(pady=6)
tk.Button(root, text="④ 自動アノテーション生成", width=70, command=run_auto_annotation).pack(pady=4)
tk.Button(root, text="⑤ LabelImg で修正 → 再学習", width=70, command=run_labelimg).pack(pady=4)
tk.Button(root, text="⑥ 再学習開始（詳細設定ダイアログ）", width=70, bg="#ffdddd",
          command=run_train_dialog).pack(pady=10)

tk.Label(root, text="【検出アプリ】", font=("Meiryo", 14, "bold")).pack(pady=12)
tk.Button(root, text="⑦ 画像検出 GUI（best.pt 使用）", width=70, command=run_detector).pack(pady=4)

root.mainloop()

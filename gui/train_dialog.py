# gui/train_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TrainDialog(tk.Toplevel):

    def __init__(self, master, env_values):
        super().__init__(master)
        self.title("学習パラメータ設定")
        self.geometry("520x540")
        self.resizable(False, False)
        self.env_values = env_values

        # ---- 各種設定値（デフォルト） ----
        self.var_device = tk.StringVar(value="GPU")
        self.var_epochs = tk.StringVar(value="150")
        self.var_batch = tk.StringVar(value="16")
        self.var_imgsz = tk.StringVar(value="640")
        self.var_lr = tk.StringVar(value="0.003")
        self.var_patience = tk.StringVar(value="20")
        self.var_pretrained = tk.StringVar(value="yolov8m.pt")
        self.var_data_yaml = tk.StringVar(value=os.path.join(BASE, "data", "object.yaml"))

        # ====================================================
        # ★ フォーム（grid レイアウト版）
        # ====================================================
        frm = tk.Frame(self)
        frm.pack(padx=20, pady=15, fill="x")

        def add_row(row, label, widget):
            tk.Label(frm, text=label, width=18, anchor="w").grid(row=row, column=0, pady=5, sticky="w")
            widget.grid(row=row, column=1, pady=5, sticky="w")

        # ---- 各入力欄 ----
        add_row(0, "デバイス (GPU/CPU)",
                ttk.Combobox(frm, textvariable=self.var_device,
                             values=["GPU", "CPU"], width=18))

        add_row(1, "Epochs", tk.Entry(frm, textvariable=self.var_epochs, width=20))
        add_row(2, "Batch size", tk.Entry(frm, textvariable=self.var_batch, width=20))
        add_row(3, "Image size", tk.Entry(frm, textvariable=self.var_imgsz, width=20))
        add_row(4, "学習率 lr0", tk.Entry(frm, textvariable=self.var_lr, width=20))
        add_row(5, "Patience", tk.Entry(frm, textvariable=self.var_patience, width=20))

        add_row(6, "事前学習モデル",
                ttk.Combobox(frm, textvariable=self.var_pretrained,
                             values=["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt"],
                             width=18))

        add_row(7, "データ設定 YAML", tk.Entry(frm, textvariable=self.var_data_yaml, width=30))

        # ---- 説明文 ----
        explanation = tk.Label(
            self,
            text=(
                "【各設定の意味】\n"
                "Epochs：学習回数。多いほど精度↑（時間↑）\n"
                "Batch size：一度に処理する画像数。多いほど速い（VRAM消費↑）\n"
                "Image size：入力画像解像度。640推奨\n"
                "学習率 lr0：学習の進みやすさ。0.003が安定\n"
                "Patience：Val loss が改善しない回数で停止\n"
                "事前学習モデル：YOLOv8 の重み\n"
            ),
            justify="left",
            anchor="w"
        )
        explanation.pack(padx=18, pady=10, fill="x")

        # ---- ボタン ----
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="学習開始", width=15, bg="#ffdddd",
                  command=self.start_training).pack(side="left", padx=10)

        tk.Button(btn_frame, text="キャンセル", width=15,
                  command=self.destroy).pack(side="left", padx=10)

        # モーダル化（親をロック）
        self.transient(master)
        self.grab_set()
        master.wait_window(self)

    # ====================================================
    # ★ 学習実行処理
    # ====================================================
    def start_training(self):
        env = os.environ.copy()

        env["TRAIN_DEVICE"] = "0" if self.var_device.get() == "GPU" else "cpu"
        env["TRAIN_EPOCHS"] = self.var_epochs.get()
        env["TRAIN_BATCH"] = self.var_batch.get()
        env["TRAIN_IMGSZ"] = self.var_imgsz.get()
        env["TRAIN_LR"] = self.var_lr.get()
        env["TRAIN_PATIENCE"] = self.var_patience.get()
        env["TRAIN_PRETRAINED"] = self.var_pretrained.get()
        env["TRAIN_DATA"] = self.var_data_yaml.get()

        env.update(self.env_values)

        train_script = os.path.join(BASE, "scripts", "train.py")

        messagebox.showinfo("開始", "学習を開始します（別ウィンドウ）。")

        subprocess.Popen([sys.executable, train_script], env=env)

        self.destroy()


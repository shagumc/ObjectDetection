import os
from datetime import datetime
import shutil
from ultralytics import YOLO

# ===========================================================
# ★ BASE PATH
# ===========================================================
BASE = os.path.dirname(os.path.abspath(__file__))     # scripts/
ROOT = os.path.dirname(BASE)                          # ObjectDetection/

# ===========================================================
# ★ GUI からの環境変数を取得
# ===========================================================
def getenv(name, default):
    return os.environ.get(name, default)

DATA_YAML = getenv("TRAIN_DATA", os.path.join(ROOT, "data", "object.yaml"))
MODELS_DIR = os.path.join(ROOT, "models")

PRETRAINED = getenv("TRAIN_PRETRAINED", "yolov8m.pt")

RUN_NAME = "train_result"

# ---- 数値系は型変換 ----
EPOCHS = int(getenv("TRAIN_EPOCHS", 100))
IMG_SIZE = int(getenv("TRAIN_IMGSZ", 640))
BATCH = int(getenv("TRAIN_BATCH", 16))
PAT = int(getenv("TRAIN_PATIENCE", 20))
LR0 = float(getenv("TRAIN_LR", 0.003))

DEVICE = getenv("TRAIN_DEVICE", "cpu")   # "0" or "cpu"


def main():

    print("=== YOLO Training Start ===")
    print("DATA YAML:", DATA_YAML)
    print("DEVICE:", DEVICE)
    print("EPOCHS:", EPOCHS)
    print("BATCH:", BATCH)
    print("IMGSZ:", IMG_SIZE)
    print("LR0:", LR0)
    print("PATIENCE:", PAT)

    os.makedirs(MODELS_DIR, exist_ok=True)

    # -----------------------------
    # ★ 事前学習モデルの読み込み
    # -----------------------------
    model = YOLO(PRETRAINED)

    # -----------------------------
    # ★ 学習
    # -----------------------------
    result = model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        patience=PAT,
        lr0=LR0,
        device=DEVICE,
        project=MODELS_DIR,
        name=RUN_NAME,
        exist_ok=True
    )

    # -----------------------------
    # ★ best.pt のパス
    # -----------------------------
    GENERATED_BEST = os.path.join(MODELS_DIR, RUN_NAME, "weights", "best.pt")

    if not os.path.exists(GENERATED_BEST):
        print("❌ best.pt が生成されませんでした")
        return

    FINAL_BEST = os.path.join(MODELS_DIR, "best.pt")

    # -----------------------------
    # ★ 既存 best.pt をバックアップ
    # -----------------------------
    if os.path.exists(FINAL_BEST):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = os.path.join(MODELS_DIR, f"best_{timestamp}.pt")
        shutil.move(FINAL_BEST, backup)
        print("📦 既存モデルを退避:", backup)

    # -----------------------------
    # ★ 新しい best.pt を配置
    # -----------------------------
    shutil.copy2(GENERATED_BEST, FINAL_BEST)
    print("✅ 新しい best.pt を配置:", FINAL_BEST)

    print("=== Training Complete ===")


if __name__ == "__main__":
    main()

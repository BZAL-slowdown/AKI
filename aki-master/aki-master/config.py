import os
from pathlib import Path


PROJECT_ROOT = Path(os.environ.get("AKI_CODE_ROOT", Path(__file__).resolve().parent)).resolve()
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "model"
RESULT_DIR = PROJECT_ROOT / "result"

MODEL_FILE = os.environ.get("AKI_MODEL_FILE", "aki_model（0.816）.pt")

SELECTED_COLS = [
    "年龄",
    "高血压",
    "糖尿病",
    "是否独肾",
    "血糖（术前）",
    "尿素氮（术前）",
    "乳酸（术前）",
    "肌酐（术前）",
    "AST（术前）",
    "中性粒细胞（术前）",
    "白细胞（术前）",
]

config = {
    "PROJECT_ROOT": str(PROJECT_ROOT),
    "TRAIN_IMG_PATH": str(DATA_DIR / "images"),
    "DATA_CSV": str(DATA_DIR / "data.xlsx"),
    "SELECTED_COLS": SELECTED_COLS,
    "MODEL_SAVE_PATH": str(MODEL_DIR / "aki_model.pt"),
    "TAB_SAVE_PATH": str(MODEL_DIR / "tab_mlp.pkl"),
    "IMG_SAVE_PATH": str(MODEL_DIR / "img_cnn.pt"),
    "MODEL_PATH": str(MODEL_DIR / MODEL_FILE),
    "RESULT_PATH": str(RESULT_DIR),
    "BATCH_SIZE": 8,
    "EPOCHS": 300,
    "LEARNING_RATE": 0.0001,
    "FOCAL_GAMMA": 0.0,
    "WEIGHT_FACTOR": 1.0,
    "RANDOM_SEED": 42,
}

MODEL_PATH = config["MODEL_PATH"]
RESULT_PATH = config["RESULT_PATH"]
DEVICE = "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu"
SHAP_THRESHOLD = 0.1

config["IMG_SIZE"] = 224
config["IMG_MEAN"] = [0.485, 0.456, 0.406]
config["IMG_STD"] = [0.229, 0.224, 0.225]

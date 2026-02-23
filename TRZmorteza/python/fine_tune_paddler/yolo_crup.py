import os
import cv2
from ultralytics import YOLO

# ===== CONFIG =====
INPUT_DIR = "to_crop"
OUTPUT_DIR = "dataset/train"

PAD_TOP = 5
PAD_BOTTOM = 5
PAD_LEFT = 35
PAD_RIGHT = 25

MIN_ROW_ASPECT_RATIO = 2.5
TARGET_TEXT_HEIGHT = 90

model = YOLO("best.pt")

# ===================

def get_class_id(box):
    try:
        return int(box.cls.item())
    except:
        return -1

def is_rectangle(box):
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    if h <= 0:
        return False
    return (w / h) >= MIN_ROW_ASPECT_RATIO

def extract_rows(img):
    results = model(img, verbose=False)
    h, w = img.shape[:2]
    rows = []

    for box in results[0].boxes:
        if get_class_id(box) != 1:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())

        if not is_rectangle([x1, y1, x2, y2]):
            continue

        x1 = max(0, x1 - PAD_LEFT)
        y1 = max(0, y1 - PAD_TOP)
        x2 = min(w, x2 + PAD_RIGHT)
        y2 = min(h, y2 + PAD_BOTTOM)

        rows.append([x1, y1, x2, y2])

    return rows

# ===== MAIN =====

os.makedirs(OUTPUT_DIR, exist_ok=True)

counter = 0

for file in os.listdir(INPUT_DIR):
    if not file.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    path = os.path.join(INPUT_DIR, file)
    img = cv2.imread(path)
    if img is None:
        continue

    rows = extract_rows(img)

    for (x1, y1, x2, y2) in rows:
        cropped = img[y1:y2, x1:x2]

        # normalize height
        h, w = cropped.shape[:2]
        scale = TARGET_TEXT_HEIGHT / h
        new_w = int(w * scale)
        resized = cv2.resize(cropped, (new_w, TARGET_TEXT_HEIGHT))

        save_path = os.path.join(OUTPUT_DIR, f"{counter}.jpg")
        cv2.imwrite(save_path, resized)

        counter += 1

print(f"Done. Total rows saved: {counter}")
import os
import cv2
from paddleocr import PaddleOCR

# ===== CONFIG =====
DATASET_DIR = "dataset/train"
LABEL_FILE = "dataset/train.txt"
PROGRESS_FILE = "dataset/progress.txt"
RUN_OCR = True   # True = auto OCR all, False = manual edit mode
# ==================

# ---- Load image list ----
images = sorted(
    [f for f in os.listdir(DATASET_DIR)
     if f.lower().endswith((".jpg", ".png", ".jpeg"))],
    key=lambda x: int(os.path.splitext(x)[0])
)

# ---- Load existing labels ----
labels = {}
if os.path.exists(LABEL_FILE):
    with open(LABEL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "\t" in line:
                path, text = line.strip().split("\t", 1)
                labels[path] = text

# ============================================================
# =================== AUTO OCR MODE ==========================
# ============================================================
if RUN_OCR:

    print("Running AUTO OCR for all images...")

    ocr = PaddleOCR(lang='ar', use_angle_cls=False)

    for i, file in enumerate(images):
        rel_path = f"train/{file}"

        # Skip if already labeled
        if rel_path in labels:
            continue

        img_path = os.path.join(DATASET_DIR, file)
        result = ocr.ocr(img_path)
        text = ""
        for block in result:
                
                for item in block['rec_texts']:
                    # text += item[1][0] + " "
                    text += item + " "
                

        
        labels[rel_path] = text

        # Save progressively (safe mode)
        with open(LABEL_FILE, "w", encoding="utf-8") as f:
            for k, v in labels.items():
                f.write(f"{k}\t{v}\n")

        print(f"OCR done: {file} text: {text.strip()}")

    print("AUTO OCR FINISHED.")
    print("Now set RUN_OCR = False and run again for manual correction.")
    exit()


# ============================================================
# =================== MANUAL LABEL MODE ======================
# ============================================================

print("Manual labeling mode...")

start_index = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        start_index = int(f.read().strip())

print(f"Resuming from index: {start_index}")

try:
    for i in range(start_index, len(images)):

        file = images[i]
        img_path = os.path.join(DATASET_DIR, file)
        rel_path = f"train/{file}"

        img = cv2.imread(img_path)

        text = labels.get(rel_path, "")

        print(f"\nImage: {file}")
        print(f"Current Label: {text}")

        cv2.imshow("Row", img)
        cv2.waitKey(1)

        new_text = input("Edit (Enter=keep): ").strip()

        if new_text:
            text = new_text

        labels[rel_path] = text

        # Save label file immediately
        with open(LABEL_FILE, "w", encoding="utf-8") as f:
            for k, v in labels.items():
                f.write(f"{k}\t{v}\n")

        # Save progress
        with open(PROGRESS_FILE, "w") as f:
            f.write(str(i + 1))

        cv2.destroyAllWindows()

except KeyboardInterrupt:
    print("\nStopped safely. Will resume next time.")

finally:
    cv2.destroyAllWindows()
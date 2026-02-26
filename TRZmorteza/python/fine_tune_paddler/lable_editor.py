import os
import cv2
from paddleocr import PaddleOCR
import ctypes
from colorama import Fore, Back, Style, init
import time
import easyocr
sp=time.sleep
init(autoreset=True)
# ===== CONFIG =====
DATASET_DIR = "dataset/train"
LABEL_FILE = "dataset/train.txt"
PROGRESS_FILE = "dataset/progress.txt"
RUN_OCR = True    # True = auto OCR all, False = manual edit mode
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
                print(line.strip().split("\t", 1))
                path, text = line.strip().split("\t", 1)
                labels[path] = text

# ============================================================
# =================== AUTO OCR MODE ==========================
# ============================================================
if RUN_OCR:

    print("Running AUTO OCR for all images...")
    reader = easyocr.Reader(['en'])  # English

    ocr = PaddleOCR(
    lang='en',
    ocr_version='PP-OCRv5'

)
    for i, file in enumerate(images):
        rel_path = f"train/{file}"

        # Skip if already labeled
        if rel_path in labels:
            continue

        img_path = os.path.join(DATASET_DIR, file)
        result_easy = reader.readtext(img_path)
        text = ""
        # if you wanna test paddler, uncomment the line above and comment the line below    
        # result = ocr.predict(img_path)
        # for block in result:
        #         for item in block['rec_texts']:
        #             text += item + " "
        # end of paddler test
        for bbox, t, confidence in result_easy:
            text += t + " "
        
        labels[rel_path] = text

        # Save progressively (safe mode)
        with open(LABEL_FILE, "w", encoding="utf-8") as f:
            for k, v in labels.items():
                f.write(f"{k}\t{v}\n")
        img = cv2.imread(img_path)
# ===========================================
        # cv2.namedWindow("Row", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Row",1350 , 200)
        # cv2.moveWindow("Row", 90, 0)
        # cv2.imshow("Row", img)
        # Windows always-on-top trick
        print(f"OCR done: {file} text: {text.strip()}")
        # input(Fore.WHITE+'did you see the image?')
        # cv2.destroyAllWindows()


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
# ===========================================
        cv2.namedWindow("Row", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Row",1350 , 200)
        cv2.moveWindow("Row", 90, 0)

        # Windows always-on-top trick
        # hwnd = cv2.getWindowHandle("Row")
        ctypes.windll.user32.SetWindowPos('hwnd', -1, 0, 0, 0, 0, 0x0001 | 0x0002)



# ===========================================
        text = labels.get(rel_path, "")
        os.system("cls" if os.name == "nt" else "clear")
        print(Fore.GREEN + f"\nImage: {file}")
        print(Fore.WHITE + f"Current Label: ",end="")
        print(Fore.YELLOW + f"{text}")
        
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
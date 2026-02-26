import os
import random
import shutil

DATASET_DIR = "dataset/train"
LABEL_FILE = "dataset/train.txt"
OUTPUT_DIR = "dataset/split"

TRAIN_COUNT = 50
VAL_COUNT = 50

# Create output folders
os.makedirs(os.path.join(OUTPUT_DIR, "train"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "val"), exist_ok=True)

# Read label lines
with open(LABEL_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

random.shuffle(lines)

train_lines = lines[:TRAIN_COUNT]
val_lines = lines[TRAIN_COUNT:TRAIN_COUNT + VAL_COUNT]

# Write new label files
with open(os.path.join(OUTPUT_DIR, "train.txt"), "w", encoding="utf-8") as f:
    f.writelines(train_lines)

with open(os.path.join(OUTPUT_DIR, "val.txt"), "w", encoding="utf-8") as f:
    f.writelines(val_lines)

# Copy images
def copy_images(lines, dest_folder):
    for line in lines:
        img_rel_path = line.strip().split("\t")[0]
        img_name = os.path.basename(img_rel_path)
        src = os.path.join(DATASET_DIR, img_name)
        dst = os.path.join(dest_folder, img_name)
        shutil.copy(src, dst)

copy_images(train_lines, os.path.join(OUTPUT_DIR, "train"))
copy_images(val_lines, os.path.join(OUTPUT_DIR, "val"))

print("✅ Split complete.")
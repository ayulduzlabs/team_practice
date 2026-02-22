from ultralytics import YOLO
import cv2
import os
import numpy as np
import requests
import logging
# from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import threading
import re
from colorama import Fore, Back, Style, init
init()
semaphore = threading.Semaphore(2)
PAD_TOP = 5
PAD_BOTTOM = 5
PAD_LEFT = 35
PAD_RIGHT = 25
MIN_ROW_ASPECT_RATIO = 2.5   
MIN_TEXT_HEIGHT = 60        
TARGET_TEXT_HEIGHT = 90     
# project_path=os.path.join(os.getcwd(),'TRZmorteza','python','yolo_ocr')
project_path=os.getcwd()
print('path:',project_path)
ocr1 = PaddleOCR(lang='fa', use_angle_cls=True)
ocr2 = PaddleOCR(lang='fa', use_angle_cls=True)


model = YOLO(os.path.join(project_path,'best.pt'))


#=====================================
def get_class_id(box):
    try:
        return int(box.cls.item())
    except:
        return -1
#=====================================
def is_rectangle(box):
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    if h <= 0:
        return False
    return (w / h) >= MIN_ROW_ASPECT_RATIO
#=====================================
def extract_rows(img, original_link=None):
    results = model(img, verbose=False)
    h, w = img.shape[:2]
    rows = []

    for idx, box in enumerate(results[0].boxes):
        if get_class_id(box) != 1:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())

        if not is_rectangle([x1, y1, x2, y2]):
            print(f"[DROP] Non-rectangular row {idx}")
            continue

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        row = {
            "box": [x1, y1, x2, y2],
            "original_link": original_link,
        }
        
        rows.append(row)

    return rows
#=====================================
def get_class_id(box):
    try:
        return int(box.cls.item())
    except:
        return -1
#=====================================
def preprocess_for_ocr(img):
    
    img = cv2.copyMakeBorder(
        img,
        PAD_TOP, PAD_BOTTOM, PAD_LEFT, PAD_RIGHT,
        cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )

    h, w = img.shape[:2]

 
    if h < MIN_TEXT_HEIGHT:
        scale = TARGET_TEXT_HEIGHT / h
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)


    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

   
    h, w = img.shape[:2]
    img = cv2.resize(img, (w, int(h * 0.85)), interpolation=cv2.INTER_LINEAR)

    return img
#=====================================
def has_table(img):
    results = model(img, verbose=False)
    for box in results[0].boxes:
        if get_class_id(box) == 0:
            return True
    return False
#=====================================
#=====================================
def ocr_worker(rows, result_container,img,count,ocr):
    try:
        print(f"Thread {count} started")
        for idx, row in enumerate(rows):
            x1, y1, x2, y2 = row["box"]
            
            # cropped = img[y1:y2, x1:x2]


            PAD = 5  # 10 pixels

            h, w = img.shape[:2]

            # expand coordinates with padding
            x1_padded = max(0, x1 - PAD)
            y1_padded = max(0, y1 - PAD)
            x2_padded = min(w, x2 + PAD)
            y2_padded = min(h, y2 + PAD)

            cropped = img[y1_padded:y2_padded, x1_padded:x2_padded]


            # path=os.path.join(os.getcwd(),count,f"cropped_{count}_{idx}.jpg")
            cv2.imwrite(f"{count}\\cropped_{count}_{idx}.jpg", cropped)
            # cv2.imshow(f"cropped_{count}_{idx}", cropped)
            ocr_result = ocr.ocr(img[y1:y2, x1:x2])
            
            # ocr needs to be purfected
            text = ""
            for block in ocr_result:
                print('block:',block)
                for item in block['rec_texts']:
                    # text += item[1][0] + " "
                    text += item + " "

            # row["text"] = text.strip()
            # row["box"]=[count,f"{count}\\cropped_{count}_{idx}.jpg"]
            result_container.append("count}\\cropped_{count}_{idx}.jpg??"+text.strip())

            print(Fore.GREEN + f"[THREAD DONE] {text.strip()}")
    except Exception as e:
        print(Fore.RED + f"[THREAD ERROR] {e}")
        
#=====================================
if __name__ == "__main__":
    img = cv2.imread('temp_downloaded_image.jpg')
    if has_table(img):
        # img=preprocess_for_ocr(img)
        rows=extract_rows(img)
        mid = len(rows) // 2
        # first_array = rows[:mid]
        # second_array = rows[mid:]
        first_array = rows[:10]
        second_array = rows[mid:mid+10]
        all_results = []
        
        threads = []
        # print('first array:',first_array[0])
    

        t1 = threading.Thread(target=ocr_worker, args=(first_array, all_results,img,1,ocr1))
        t2 = threading.Thread(target=ocr_worker, args=(second_array, all_results,img,2,ocr2))

        threads.append(t1)
        threads.append(t2)

        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

        # ocr_worker(first_array, all_results,img,1)
        # ocr_worker(second_array, all_results,img,2)
        
        os.system('cls')
        print('=' * 50)
        print(f'len of first array: {len(first_array)}\nlen of second array: {len(second_array)}\nTotal rows: {len(rows)}')
        print('=' * 50)
        # for t in threads:
        #     # print(Fore.GREEN+'starting to join thread no:',i)
        #     t.join()
        with open('results.txt', 'w', encoding='utf-8') as f:
            for res in all_results:
                f.write(f"{res}\n")
        
        print("FINAL RESULTS:", all_results)
        #=========debug===================
        # print('extracted rows:',len(rows))
        # result = ocr.ocr(preprocess_for_ocr(img))
        # text=''
        # for blk in result:
        #     for item in blk:
        #         print('item:',item[1][0])#true item value is here
        #=========debug===================
    else:
        print('image has no price table so ignoring it')
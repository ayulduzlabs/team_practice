from ultralytics import YOLO
import cv2
import os
import numpy as np
import requests
import logging
# from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import re
from colorama import Fore, Back, Style, init
init()
PAD_TOP = 5
PAD_BOTTOM = 5
PAD_LEFT = 25
PAD_RIGHT = 25
MIN_ROW_ASPECT_RATIO = 2.5   
MIN_TEXT_HEIGHT = 60        
TARGET_TEXT_HEIGHT = 90     
# project_path=os.path.join(os.getcwd(),'TRZmorteza','python','yolo_ocr')
project_path=os.getcwd()
print('path:',project_path)
ocr = PaddleOCR(lang='fa')


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
img = cv2.imread('temp_downloaded_image.jpg')
if has_table(img):
    rows=extract_rows(img)
    #=========debug===================
    # result = ocr.ocr(preprocess_for_ocr(img))
    # text=''
    # for blk in result:
    #     for item in blk:
    #         print('item:',item[1][0])#true item value is here
    #=========debug===================
else:
    print('image has no price table so ignoring')
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

img = cv2.imread('temp_downloaded_image.jpg')
result = ocr.ocr(preprocess_for_ocr(img))
text=''
for blk in result:
  
    for item in blk:
        
        # text+= item[1][0]
        print('item:',item[1][0])#true item value is here
     
     
print(text)
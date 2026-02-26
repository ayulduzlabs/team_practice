import os
import cv2
from paddleocr import PaddleOCR
import easyocr
import ctypes
from colorama import Fore, Back, Style, init
import time
from PIL import Image
reader = easyocr.Reader(['en'])  # English
ocr = PaddleOCR(
lang='en',
ocr_version='PP-OCRv5'

)
line="==============================\n"
text = ""
start_time = time.time()
# result = ocr.predict('to_crop/3.jpg')
for i in range(0,100):
    path=f'dataset/train/{i}.jpg'
    img=cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    bw_3ch = cv2.cvtColor(bw, cv2.COLOR_GRAY2BGR)
    # cv2.imshow("img",bw_3ch)
    
# OCR
    result = ocr.predict(img)
    result_easy = reader.readtext(bw)
    text_easy = "" 
    for bbox, text, confidence in result_easy:
        text_easy += text + " "
    print("="*6,f"image number:{i}","="*6)
    print(Fore.CYAN + "EasyOCR Result:")
    print(text_easy,end="")    
    print(Style.RESET_ALL,end="")
    for block in result:
                    for item in block['rec_texts']:
                        text += item + " "
                    
    print(Fore.GREEN + "\nPaddleOCR Result:")
    print(text)
    print(Style.RESET_ALL,end="")
   
    # cv2.waitKey(1)
print(Fore.YELLOW + "Total time taken: " + str(time.time() - start_time) + " seconds")
# print(result)
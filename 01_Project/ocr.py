# -*- coding: utf-8 -*-
 
import pytesseract
from PIL import Image
import sys
import time
import cv2

reload(sys)
sys.setdefaultencoding('utf-8')

from aip import AipOcr

APP_ID = '11469668'
API_KEY = 'G7L1f1IOd9x8uvXXijam7k1o'
SECRET_KEY = 'rb4hhAlngY7vjd8EPXkRdHvBGNBQN0ZV'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def ocr2(path):
    tmp = Image.open(path)
    tmp.load()
    result = ''
    result = pytesseract.image_to_string(tmp,lang='chi_sim+eng')
    return result

def ocr(path):
    result = ''
    try:
        tmp = open(path,'rb').read()
        ocr = client.basicGeneral(tmp)
        if ocr != None and len(ocr)>0:
            print(ocr)
            for w in ocr['words_result']:
                if w != None:
                    result = result + w['words']
    except:
		result = ''
    return result

def main(argv):
    filepath=unicode(argv[0],'utf8')
    result = ocr(filepath)
    print result

if __name__ == '__main__':
    main(sys.argv[1:])
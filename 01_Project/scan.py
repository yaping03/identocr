#! -*- coding:utf-8 -*-

import cv2
import sys
import imutils
from imutils import contours
import numpy as np
import os
from datetime import datetime
import random
import collections
import ocr
import re
import time
import locale
import threading
import Queue

reload(sys)
sys.setdefaultencoding('utf-8')

# 图片缩放尺寸
RESIZE_IMAGE_WIDTH = 1800

# 识别标准块二值化取值参数
BLOCK_THRESHOLD_THRESH = 127
BLOCK_THRESHOLD_MAXVAL = 255

# 识别标准块腐蚀膨胀核大小尺寸
BLOCK_NORMAL_BLOCK_SIZE = 4

# 识别标准块面积
BLOCK_NORMAL_BLOCK_AREA = 80
BLOCK_NORMAL_BLOCK_AREA_MAX = 2000
BLOCK_NORMAL_BLOCK_WIDTH = 30
BLOCK_NORMAL_BLOCK_HEIGHT = 30

BLOCK_A_NORMAL_BLOCK_AREA = 300
BLOCK_A_NORMAL_BLOCK_AREA_MAX = 2000
BLOCK_A_NORMAL_BLOCK_WIDTH = 20
BLOCK_A_NORMAL_BLOCK_WIDTH_MAX = 80
BLOCK_A_NORMAL_BLOCK_HEIGHT = 10
BLOCK_A_NORMAL_BLOCK_HEIGHT_MAX = 45

BLOCK_B_NORMAL_BLOCK_AREA = 300
BLOCK_B_NORMAL_BLOCK_AREA_MAX = 2000
BLOCK_B_NORMAL_BLOCK_WIDTH = 20
BLOCK_B_NORMAL_BLOCK_WIDTH_MAX = 80
BLOCK_B_NORMAL_BLOCK_HEIGHT = 10
BLOCK_B_NORMAL_BLOCK_HEIGHT_MAX = 45

# 识别表格二值化取值参数
GRID_THRESHOLD_THRESH = 200
GRID_THRESHOLD_MAXVAL = 255

# 识别表格腐蚀膨胀核大小尺寸
GRID_NORMAL_BLOCK_SIZE = 1

# 识别文字二值化取值参数
TEXT_THRESHOLD_THRESH = 200
TEXT_THRESHOLD_MAXVAL = 255

# 识别文字腐蚀膨胀核大小尺寸
TEXT_NORMAL_BLOCK_SIZE = 4

def get_image_by_path(path):
    source = cv2.imread(path)
    resize = imutils.resize(source, width = RESIZE_IMAGE_WIDTH)

    return resize

def get_block(source,cmd_debug=False):
    # 灰度
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # 二值化
    retval, threshold = cv2.threshold(gray, BLOCK_THRESHOLD_THRESH, BLOCK_THRESHOLD_MAXVAL, cv2.THRESH_BINARY_INV)
    # 核大小
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(BLOCK_NORMAL_BLOCK_SIZE, BLOCK_NORMAL_BLOCK_SIZE))
    # 腐蚀
    erode = cv2.erode(threshold,kernel)
    # 膨胀
    dilate = cv2.dilate(erode,kernel)
    # 轮廓
    contour, cnts, hierarchy = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if(cmd_debug):
        print(len(cnts))

        for ci,cnt in enumerate(cnts):
            cv2.drawContours(source, cnt, -1, (0, 255, 0), 2)

        # cv2.imshow('view', source)
        # cv2.waitKey(0)

    return cnts

def get_grid(source,cmd_debug=False):
    # 灰度
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # 二值化
    retval, threshold = cv2.threshold(gray, GRID_THRESHOLD_THRESH, GRID_THRESHOLD_MAXVAL, cv2.THRESH_BINARY_INV)
    # 核大小
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (GRID_NORMAL_BLOCK_SIZE, GRID_NORMAL_BLOCK_SIZE))
    # 腐蚀
    erode = cv2.erode(threshold,kernel)
    # 轮廓
    contour, cnts, hierarchy = cv2.findContours(erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    if(cmd_debug):
        cv2.drawContours(source, cnts[0], -1, (0, 255, 0), 2)
        cv2.imshow('view', source)
        cv2.waitKey(0)

    return cnts[0]

def get_top_count(cnts,grid=None,cmd_debug=False):
    count = 0
    cnts_orign_sorts, cnts_pos = contours.sort_contours(cnts, method="top-to-bottom")
    cnts_sorts = []
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, cnts_orign in enumerate(cnts_orign_sorts):
        (x,y,w,h) = cv2.boundingRect(cnts_orign)
        if grid is not None and x > gx-10 and x < gx+gw+10 and y > gy-10 and y < gy+10:
            continue
        area = cv2.contourArea(cnts_orign)
        if area > BLOCK_NORMAL_BLOCK_AREA and area < BLOCK_NORMAL_BLOCK_AREA_MAX:
            cnts_sorts.append(cnts_orign)
    cnts_target = cnts_sorts[0]
    (target_x,target_y,target_width,target_height) = cv2.boundingRect(cnts_target)
    target_rect = cv2.minAreaRect(cnts_target)
    target_center_x,target_center_y = target_rect[0]
    for i, c in enumerate(cnts_sorts):
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if cmd_debug:
            print ('get_top_count',center_x,center_y,area,'---------',target_center_x,target_center_y,'|||',target_center_y - target_height/2 - 10,target_center_y + target_height/2 + 10)
        if (center_y >= target_center_y - target_height/2 - 10 and center_y <= target_center_y + target_height/2 + 10):
            count = count + 1
    return count

def get_bottom_count(cnts,grid=None,iw=0,ih=0,cmd_debug=False):
    count = 0
    cnts_orign_sorts, cnts_pos = contours.sort_contours(cnts, method="bottom-to-top")
    cnts_sorts = []
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, cnts_orign in enumerate(cnts_orign_sorts):
        (x,y,w,h) = cv2.boundingRect(cnts_orign)
        area = cv2.contourArea(cnts_orign)
        if cmd_debug:
            print (i,'get_bottom_count',x,y,area,'---------',gx-10,iw-20,gy-10,ih-20)
        if x > gx-10 and x < iw-20 and y > gy-10 and y < ih-20:
            if cmd_debug:
                print 'yes'
            if area > BLOCK_NORMAL_BLOCK_AREA and area < BLOCK_NORMAL_BLOCK_AREA_MAX:
                cnts_sorts.append(cnts_orign)
        else:
            if cmd_debug:
                print 'no'
    cnts_target = cnts_sorts[0]
    (target_x,target_y,target_width,target_height) = cv2.boundingRect(cnts_target)
    target_rect = cv2.minAreaRect(cnts_target)
    target_center_x,target_center_y = target_rect[0]
    for i, c in enumerate(cnts_sorts):
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if cmd_debug:
            print ('get_bottom_count_top_count',center_x,center_y,area,'---------',target_center_x,target_center_y,'|||',target_center_y - target_height/2 - 10,target_center_y + target_height/2 + 10)
        if (center_y >= target_center_y - target_height/2 - 10 and center_y <= target_center_y + target_height/2 + 10):
            count = count + 1
    return count

def get_bottom_blocks(cnts,doc_type=2,grid=None,iw=0,ih=0,cmd_debug=False):
    blocks = []
    cnts_orign_sorts, cnts_pos = contours.sort_contours(cnts, method="bottom-to-top")
    cnts_sorts = []
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, cnts_orign in enumerate(cnts_orign_sorts):
        (x,y,w,h) = cv2.boundingRect(cnts_orign)
        area = cv2.contourArea(cnts_orign)
        if cmd_debug:
            print (i,'get_bottom_count',x,y,area,'---------',gx-10,iw-20,gy-10,ih-20)
        if x > gx-10 and x < iw-20 and y > gy-10 and y < ih-20:
            if cmd_debug:
                print 'yes'
            if doc_type==1:
                if area > BLOCK_A_NORMAL_BLOCK_AREA:
                    cnts_sorts.append(cnts_orign)
            else:
                if area > BLOCK_B_NORMAL_BLOCK_AREA:
                    cnts_sorts.append(cnts_orign)
        else:
            if cmd_debug:
                print 'no'
    cnts_target = cnts_sorts[0]
    (target_x,target_y,target_width,target_height) = cv2.boundingRect(cnts_target)
    target_rect = cv2.minAreaRect(cnts_target)
    target_center_x,target_center_y = target_rect[0]
    for i, c in enumerate(cnts_sorts):
        area = cv2.contourArea(c)
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if cmd_debug:
            print ('get_bottom_blocks',center_x,center_y,area,'---------',target_center_x,target_center_y,'|||',target_center_y - target_height/2 - 10,target_center_y + target_height/2 + 10)
        if (center_y >= target_center_y - target_height/2 - 10 and center_y <= target_center_y + target_height/2 + 10):
            blocks.append(c)
            if cmd_debug:
                print ('yes')
        else:
            if cmd_debug:
                print ('no')
    blocks_sorts, blocks_pos = contours.sort_contours(blocks, method="left-to-right")
    return blocks_sorts

def get_left_count(cnts,grid=None,cmd_debug=False):
    count = 0
    cnts_orign_sorts, cnts_pos = contours.sort_contours(cnts, method="left-to-right")
    cnts_sorts = []
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, cnts_orign in enumerate(cnts_orign_sorts):
        (x,y,w,h) = cv2.boundingRect(cnts_orign)
        area = cv2.contourArea(cnts_orign)
        if grid is not None and x > gx-10 and x < gx+gw+10 and y > gy-10 and y < gy+10:
            continue
        area = cv2.contourArea(cnts_orign)
        if cmd_debug:
            print (i,'get_left_count',x,y,area,'---------',gx-10,gx+gw+10,gy-5,gy+5,(grid is not None and x > gx-10 and x < gx+gw+10 and y > gy-5 and y < gy+5),area > BLOCK_NORMAL_BLOCK_AREA)
        if grid is not None and x > gx-10 and x < gx+gw+10 and y > gy-5 and y < gy+5:
            continue
        if area > BLOCK_NORMAL_BLOCK_AREA and area < BLOCK_NORMAL_BLOCK_AREA_MAX:
            cnts_sorts.append(cnts_orign)
    cnts_target = cnts_sorts[0]
    (target_x,target_y,target_width,target_height) = cv2.boundingRect(cnts_target)
    target_rect = cv2.minAreaRect(cnts_target)
    target_center_x,target_center_y = target_rect[0]
    for i, c in enumerate(cnts_sorts):
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        area = cv2.contourArea(c)
        if cmd_debug:
            print ('get_left_count',center_x,center_y,area,'---------',target_center_x,target_center_y,'|||',target_center_x - target_width/2 - 10,target_center_x + target_width/2 + 10)
        if (center_x >= target_center_x - target_width/2 - 10 and center_x <= target_center_x + target_width/2 + 10):
            count = count + 1
            if cmd_debug:
                print i,'yes'
        else:
            if cmd_debug:
                print i,'no'
    return count

def get_right_count(cnts,grid=None,iw=0,ih=0,cmd_debug=False):
    count = 0
    cnts_orign_sorts, cnts_pos = contours.sort_contours(cnts, method="right-to-left")
    cnts_sorts = []
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, cnts_orign in enumerate(cnts_orign_sorts):
        (x,y,w,h) = cv2.boundingRect(cnts_orign)
        area = cv2.contourArea(cnts_orign)
        if cmd_debug:
            print (i,'get_right_count',x,y,area,'---------',gx-10,iw-20,gy-10,ih-20)
        if x > gx-10 and x < iw-20 and y > gy-10 and y < ih-20:
            if cmd_debug:
                print 'yes'
            if area > BLOCK_NORMAL_BLOCK_AREA and area < BLOCK_NORMAL_BLOCK_AREA_MAX:
                cnts_sorts.append(cnts_orign)
        else:
            if cmd_debug:
                print 'no'
    cnts_target = cnts_sorts[0]
    (target_x,target_y,target_width,target_height) = cv2.boundingRect(cnts_target)
    target_rect = cv2.minAreaRect(cnts_target)
    target_center_x,target_center_y = target_rect[0]
    for i, c in enumerate(cnts_sorts):
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        area = cv2.contourArea(c)
        if cmd_debug:
            print ('get_right_count',center_x,center_y,area,'---------',target_center_x,target_center_y,'|||',target_center_x - target_width/2 - 10,target_center_x + target_width/2 + 10)
        if (center_x >= target_center_x - target_width/2 - 10 and center_x <= target_center_x + target_width/2 + 10):
            count = count + 1
            if cmd_debug:
                print i,'yes'
        else:
            if cmd_debug:
                print i,'no'
    return count

def get_right_blocks(cnts,doc_type=2,grid=None,iw=0,ih=0,cmd_debug=False):
    blocks = []
    cnts_orign_sorts, cnts_pos = contours.sort_contours(cnts, method="right-to-left")
    cnts_sorts = []
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, cnts_orign in enumerate(cnts_orign_sorts):
        (x,y,w,h) = cv2.boundingRect(cnts_orign)
        area = cv2.contourArea(cnts_orign)
        if cmd_debug:
            print (i,'get_right_count',x,y,area,'---------',gx-10,iw-20,gy-10,ih-20)
        if x > gx-10 and x < iw-20 and y > gy-10 and y < ih-20:
            if cmd_debug:
                print 'yes'
            if doc_type==1:
                if area > BLOCK_A_NORMAL_BLOCK_AREA:
                    cnts_sorts.append(cnts_orign)
            else:
                if area > BLOCK_B_NORMAL_BLOCK_AREA:
                    cnts_sorts.append(cnts_orign)
        else:
            if cmd_debug:
                print 'no'
    cnts_target = cnts_sorts[0]
    (target_x,target_y,target_width,target_height) = cv2.boundingRect(cnts_target)
    target_rect = cv2.minAreaRect(cnts_target)
    target_center_x,target_center_y = target_rect[0]
    for i, c in enumerate(cnts_sorts):
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if cmd_debug:
            print ('get_right_blocks',center_x,center_y,area,'---------',target_center_x,target_center_y,'|||',target_center_x - target_width/2 - 10,target_center_x + target_width/2 + 10)
        if (center_x >= target_center_x - target_width/2 - 10 and center_x <= target_center_x + target_width/2 + 10):
            blocks.append(c)
            if cmd_debug:
                print ('yes')
        else:
            if cmd_debug:
                print ('no')
    blocks_sorts, blocks_pos = contours.sort_contours(blocks, method="top-to-bottom")
    return blocks_sorts

def get_answer_blocks(cnts,grid,doc_type=2,cmd_debug=False):
    blocks = []
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, c in enumerate(cnts):
        (x,y,w,h) = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if cmd_debug:
            print (i,'get_answer_blocks',x,y,w,h,area,'---------',gx + 10,gx + gw - 10,gy + 10,gy + gh - 10)
        if doc_type==1:
            if area < BLOCK_A_NORMAL_BLOCK_AREA:
                continue
            if area > BLOCK_A_NORMAL_BLOCK_AREA_MAX:
                continue
            if w < BLOCK_A_NORMAL_BLOCK_WIDTH:
                continue
            if w > BLOCK_A_NORMAL_BLOCK_WIDTH_MAX:
                continue
            if h < BLOCK_A_NORMAL_BLOCK_HEIGHT:
                continue
            if h > BLOCK_A_NORMAL_BLOCK_HEIGHT_MAX:
                continue
        else:
            if area < BLOCK_B_NORMAL_BLOCK_AREA:
                continue
            if area > BLOCK_B_NORMAL_BLOCK_AREA_MAX:
                continue
            if w < BLOCK_B_NORMAL_BLOCK_WIDTH:
                continue
            if w > BLOCK_B_NORMAL_BLOCK_WIDTH_MAX:
                continue
            if h < BLOCK_B_NORMAL_BLOCK_HEIGHT:
                continue
            if h > BLOCK_B_NORMAL_BLOCK_HEIGHT_MAX:
                continue
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if (center_x >= gx + 10) and (center_x <= gx+gw - 10) and (center_y >= gy + 10) and (center_y <= gy+gh - 10):
        # if (((x > gx and x < gx+gw) or (x+w > gx and x+w < gx+gw) or (center_x > gx and center_x < gx+gw)) and ((y > gy and y < gy+gh) or (y+h > gy and y+h < gy+gh) or (center_y > gy and center_y < gy+gh))):
            # if cmd_debug:
            #     print ('get_answer_blocks',center_x,center_y,area,'---------',gx,gy,gw,gh,'|||',gx + 10,gx+gw - 10,gy + 10,gy+gh - 10)
            blocks.append(c)
            if cmd_debug:
                print ('yes')
        else:
            if cmd_debug:
                print ('no')
    if len(blocks)>0:
        blocks, cnts_pos = contours.sort_contours(blocks, method="top-to-bottom")
        blocks, cnts_pos = contours.sort_contours(blocks, method="left-to-right")
    return blocks

def get_block_by_row_and_col(blocks,block_row,block_col,doc_type=2,grid=None,cmd_debug=False):
    block = None
    (row_x,row_y,row_width,row_height) = cv2.boundingRect(block_row)
    row_center_x,row_center_y = cv2.minAreaRect(block_row)[0]
    (col_x,col_y,col_width,col_height) = cv2.boundingRect(block_col)
    col_center_x,col_center_y = cv2.minAreaRect(block_col)[0]
    if grid is not None:
        (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, c in enumerate(blocks):
        (x,y,w,h) = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if cmd_debug:
            print (i,'get_block_by_row_and_col','x',x,'y',y,'w',w,'h',h,'area',area,'---------',gx + 10,gx + gw - 10,gy + 10,gy + gh - 10)
        if doc_type==1:
            if area < BLOCK_A_NORMAL_BLOCK_AREA:
                continue
            if area > BLOCK_A_NORMAL_BLOCK_AREA_MAX:
                continue
            if w < BLOCK_A_NORMAL_BLOCK_WIDTH:
                continue
            if w > BLOCK_A_NORMAL_BLOCK_WIDTH_MAX:
                continue
            if h < BLOCK_A_NORMAL_BLOCK_HEIGHT:
                continue
            if h > BLOCK_A_NORMAL_BLOCK_HEIGHT_MAX:
                continue
        else:
            if area < BLOCK_B_NORMAL_BLOCK_AREA:
                continue
            if area > BLOCK_B_NORMAL_BLOCK_AREA_MAX:
                continue
            if w < BLOCK_B_NORMAL_BLOCK_WIDTH:
                continue
            if w > BLOCK_B_NORMAL_BLOCK_WIDTH_MAX:
                continue
            if h < BLOCK_B_NORMAL_BLOCK_HEIGHT:
                continue
            if h > BLOCK_B_NORMAL_BLOCK_HEIGHT_MAX:
                continue
        (cnt_x,cnt_y,cnt_width,cnt_height) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if cmd_debug:
            print ('get_block_by_row_and_col',center_x,center_y,area,'---------',col_center_x,col_center_y,'---------',row_center_x,row_center_y,'||',col_center_x - col_width/2 - 10,col_center_x + col_width/2 + 10,'||',row_center_y - row_height/2 - 10,row_center_y + row_height/2 + 10)
        # 1. center in x1,x2
        # 2. x1 in x1,x2
        # 3. x2 in x1,x2
        # col_x < cnt_x < col_x+col_width
        # col_x < cnt_x+cnt_width < col_x+col_width
        # col_x < center_x < col_x+col_width
        # row_y < cnt_y < row_y+row_height
        # row_y < cnt_y+cnt_height < row_y+row_height
        # row_y < center_y < row_y+row_height
        # if (center_x > col_center_x - col_width/2 - 5 and center_x < col_center_x + col_width/2 + 5) and (center_y > row_center_y - row_height/2 - 5 and center_y < row_center_y + row_height/2 + 5):
        if (((cnt_x > col_x +5 and cnt_x < col_x+col_width -5) or (cnt_x+cnt_width > col_x and cnt_x+cnt_width < col_x+col_width) or (center_x > col_x and center_x < col_x+col_width)) and ((cnt_y > row_y and cnt_y < row_y+row_height) or (cnt_y+cnt_height > row_y and cnt_y+cnt_height < row_y+row_height) or (center_y > row_y and center_y < row_y+row_height))):
            block = c
            if cmd_debug:
                print ('yes')
            break
        else:
            if cmd_debug:
                print ('no')
    return block

def get_type_blocks(cnts,grid,doc_type=2,cmd_debug=False):
    blocks = []
    (gx,gy,gw,gh) = cv2.boundingRect(grid)
    for i, c in enumerate(cnts):
        area = cv2.contourArea(c)
        if doc_type==1:
            if area < BLOCK_A_NORMAL_BLOCK_AREA:
                continue
        else:
            if area < BLOCK_B_NORMAL_BLOCK_AREA:
                continue
            # if area > BLOCK_B_NORMAL_BLOCK_AREA_MAX:
            #     continue
        (x,y,w,h) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if (center_x >= gx + 10) and (center_x <= gx+gw - 10) and (center_y >= gy + 10) and (center_y <= gy+gh - 10):
        # if (((x > gx and x < gx+gw) or (x+w > gx and x+w < gx+gw) or (center_x > gx and center_x < gx+gw)) and ((y > gy and y < gy+gh) or (y+h > gy and y+h < gy+gh) or (center_y > gy and center_y < gy+gh))):
            if cmd_debug:
                print ('get_answer_blocks',center_x,center_y,area,'---------',gx,gy,gw,gh,'|||',gx + 10,gx+gw - 10,gy + 10,gy+gh - 10)
            blocks.append(c)
            if cmd_debug:
                print ('yes')
        else:
            if cmd_debug:
                print ('no')
    if len(blocks)>0:
        blocks, cnts_pos = contours.sort_contours(blocks, method="top-to-bottom")
        blocks, cnts_pos = contours.sort_contours(blocks, method="left-to-right")
    return blocks

def get_type_by_row_and_col(blocks,block_row,block_col,doc_type=2,cmd_debug=False):
    block = None
    (row_x,row_y,row_width,row_height) = cv2.boundingRect(block_row)
    row_center_x,row_center_y = cv2.minAreaRect(block_row)[0]
    (col_x,col_y,col_width,col_height) = cv2.boundingRect(block_col)
    col_center_x,col_center_y = cv2.minAreaRect(block_col)[0]
    for i, c in enumerate(blocks):
        area = cv2.contourArea(c)
        if doc_type==1:
            if area < BLOCK_A_NORMAL_BLOCK_AREA:
                continue
        else:
            if area < BLOCK_B_NORMAL_BLOCK_AREA:
                continue
        (cnt_x,cnt_y,cnt_width,cnt_height) = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        if cmd_debug:
            print ('get_block_by_row_and_col',center_x,center_y,area,'---------',col_center_x,col_center_y,'---------',row_center_x,row_center_y,'||',col_center_x - col_width/2 - 10,col_center_x + col_width/2 + 10,'||',row_center_y - row_height/2 - 10,row_center_y + row_height/2 + 10)
        # 1. center in x1,x2
        # 2. x1 in x1,x2
        # 3. x2 in x1,x2
        # col_x < cnt_x < col_x+col_width
        # col_x < cnt_x+cnt_width < col_x+col_width
        # col_x < center_x < col_x+col_width
        # row_y < cnt_y < row_y+row_height
        # row_y < cnt_y+cnt_height < row_y+row_height
        # row_y < center_y < row_y+row_height
        # if (center_x > col_center_x - col_width/2 - 5 and center_x < col_center_x + col_width/2 + 5) and (center_y > row_center_y - row_height/2 - 5 and center_y < row_center_y + row_height/2 + 5):
        if (((cnt_x > col_x +5 and cnt_x < col_x+col_width -5) or (cnt_x+cnt_width > col_x and cnt_x+cnt_width < col_x+col_width) or (center_x > col_x and center_x < col_x+col_width)) and ((cnt_y > row_y and cnt_y < row_y+row_height) or (cnt_y+cnt_height > row_y and cnt_y+cnt_height < row_y+row_height) or (center_y > row_y and center_y < row_y+row_height))):
            block = c
            if cmd_debug:
                print ('yes')
            break
        else:
            if cmd_debug:
                print ('no')
    return block

def crop_image(image,scope,cmd_debug=False):
    x1 = scope[0]
    x2 = scope[1]
    y1 = scope[2]
    y2 = scope[3]
    img = image[y1:y2,x1:x2]
    return img

def get_rotated_image(image,grid,cmd_debug=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    angle_grid = cv2.minAreaRect(grid)[-1]

    rotated = image

    if cmd_debug:
        print '1111111'
        print angle
        print angle_grid

    if (angle_grid != 0.0 and angle < -88):
        if(angle < -45):
            angle = -(90+angle)
        else:
            angle = -angle
    
        (h,w) = image.shape[:2]
        center = (w//2,h//2)
        M = cv2.getRotationMatrix2D(center,angle,1.0)
        rotated = cv2.warpAffine(image, M, (w,h),flags = cv2.INTER_CUBIC,borderMode = cv2.BORDER_REPLICATE)

    if cmd_debug:
        print '2222222'
        print angle

    return rotated,angle

def ident(filepath,cmd_debug=False):
    
    if(os.path.exists(filepath)):
        result = {}

        if(cmd_debug):
            print(filepath)

        source = get_image_by_path(filepath)

        if(cmd_debug):
            cv2.imshow('view', source)
            cv2.waitKey(0)

        grid = get_grid(source)

        cv2.drawContours(source, [grid], -1, (0, 255, 0), 2)
        if cmd_debug:
            cv2.imshow('view', source)
            cv2.waitKey(0)

        # 图片角度纠偏
        source,angle = get_rotated_image(source,grid,cmd_debug)

        if cmd_debug:
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print("angle: {:.3f}".format(angle))

            cv2.imshow('view', source)
            cv2.waitKey(0)

        grid = get_grid(source)

        blocks = get_block(source)

        size = source.shape
        iw = size[1]
        ih = size[0]

        if cmd_debug:
            print (iw,ih)

        top_count = get_top_count(blocks,grid)
        right_count = get_right_count(blocks,grid,iw,ih)
        bottom_count = get_bottom_count(blocks,grid,iw,ih)
        left_count = get_left_count(blocks,grid)

        if(cmd_debug):
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print (top_count,right_count,bottom_count,left_count)
            
            # cv2.imshow('view', source)
            # cv2.waitKey(0)

        # 1:A,2:B
        doc_type = 0
        # 方向 1:top 2:right 3:bottom 4:left
        doc_directory = 0

        max_count = max(left_count,right_count,top_count,bottom_count)
        #print('max_count:',max_count)
        #print('left_count:',left_count)
        #print('right_count:',right_count)
        #print('top_count:',top_count)
        #print('bottom_count:',bottom_count)
        if max_count >= 30:
            doc_type = 2
            if(cmd_debug):
                print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                print "B"
        elif max_count >= 16:
            doc_type = 1
            if(cmd_debug):
                print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                print "A"
        
        if doc_type == 1:
            if left_count == 16:
                if bottom_count == max(right_count,top_count,bottom_count):
                    doc_directory = 4
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "left"

            if right_count == 16:
                if top_count == max(left_count,top_count,bottom_count):
                    doc_directory = 2
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "right"
            
            if top_count == 16:
                if left_count == max(left_count,right_count,bottom_count):
                    doc_directory = 1
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "top"

            if bottom_count == 16:
                if right_count == max(left_count,right_count,top_count):
                    doc_directory = 3
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "bottom"
        else:
            if left_count == 20:
                if bottom_count == max(right_count,top_count,bottom_count):
                    doc_directory = 4
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "left"

            if right_count == 20:
                if top_count == max(left_count,top_count,bottom_count):
                    doc_directory = 2
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "right"
            
            if top_count == 20:
                if left_count == max(left_count,right_count,bottom_count):
                    doc_directory = 1
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "top"

            if bottom_count == 20:
                if right_count == max(left_count,right_count,top_count):
                    doc_directory = 3
                    if(cmd_debug):
                        print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        print "bottom"

        # 纠正到正确方向
        if doc_directory == 1:
            source = np.rot90(source)
            source = np.rot90(source)

        elif doc_directory == 2:
            source = np.rot90(source)
            source = np.rot90(source)
            source = np.rot90(source)

        elif doc_directory == 4:
            source = np.rot90(source)

        # 重新构图
        image = source.copy()

        grid = get_grid(image)

        cv2.drawContours(image, [grid], -1, (0, 255, 0), 2)

        if cmd_debug:
            cv2.imshow('view', image)
            cv2.waitKey(0)
        
        # 图片角度纠偏
        rotated,angle = get_rotated_image(image,grid,cmd_debug)

        if cmd_debug:
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print("angle: {:.3f}".format(angle))
            cv2.imshow('view', rotated)
            cv2.waitKey(0)

        blocks = get_block(rotated)

        grid = get_grid(rotated)

        cv2.drawContours(rotated, [grid], -1, (0, 255, 0), 2)
        if cmd_debug:
            cv2.imshow('view', rotated)
            cv2.waitKey(0)

        (x,y,w,h) = cv2.boundingRect(grid)

        if(cmd_debug):
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print ('grid','width=', w, 'height=', h, 'x=', x, 'y=', y)
            # cv2.imshow('view', rotated)
            # cv2.waitKey(0)

        # 标题图片
        header_image = crop_image(rotated,[x,x+w,0,y])
        if(cmd_debug):
            cv2.imshow('view', header_image)
            cv2.waitKey(0)

        gray = cv2.fastNlMeansDenoisingColored(header_image, None, 10, 3, 3, 3)
        coefficients = [0, 1, 1]
        m = np.array(coefficients).reshape((1, 3))
        gray = cv2.transform(gray, m)

        # cv2.imshow('view', gray)
        # cv2.waitKey(0)

        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        ele = cv2.getStructuringElement(cv2.MORPH_RECT, (42, 20))
        dilation = cv2.dilate(binary, ele, iterations=1)

        # cv2.imshow('view', dilation)
        # cv2.waitKey(0)

        img, cnts, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        title_cnts = []

        for i in range(len(cnts)):
            cnt = cnts[i]
            # 计算该轮廓的面积
            area = cv2.contourArea(cnt)

            # 面积小的都筛选掉
            if (area < 100):
                continue

            # 轮廓近似，作用很小
            epsilon = 0.001 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # 找到最小的矩形，该矩形可能有方向
            rect = cv2.minAreaRect(cnt)

            (x,y,w,h) = cv2.boundingRect(cnt)

            # box是四个点的坐标
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # 计算高和宽
            height = abs(box[0][1] - box[2][1])
            width = abs(box[0][0] - box[2][0])

            title_cnts.append(cnt)

        cnts_orign_sorts, cnts_pos = contours.sort_contours(title_cnts, method="left-to-right")

        cnts_orign_sorts, cnts_pos = contours.sort_contours(cnts_orign_sorts, method="top-to-bottom")

        for ci,cnt in enumerate(cnts_orign_sorts):

            # cv2.drawContours(header_image, [box], -1, (0, 255, 0), 2)

            (x,y,w,h) = cv2.boundingRect(cnt)

            # delete by yelong 部门、年份识别，不再使用汉字识别
            # tmp = crop_image(header_image,[x,x+w,y,y+h])

            # tmp_file = "ocr_tmp_"+time.strftime("%Y%m%d%H%M%S",time.localtime())+'_'+(''.join(random.choice('abcdefghijklmn') for _ in range(5)))+'.jpg'
            # cv2.imwrite(tmp_file, tmp)
            # header_title = ocr.ocr(tmp_file).replace(' ', '')
            # os.remove(tmp_file)

            # if(cmd_debug):
            #     print 'title--------------'
            #     print header_title

            #     print (header_title[0:4],u'单位名称',u'考评年度')

            # if header_title[0:4] == u'单位名称':
            #     result['org'] = header_title
            #     print 'yes'
            # elif header_title.find(u'名称:') > -1:
            #     result['org'] = u'单位名称:'+header_title[header_title.find(u'名称:')+3:]
            #     print 'yes'

            # if header_title[0:4] == u'考评年度':
            #     result['date'] = header_title
            #     print 'yes'
            # elif header_title.find(u'年度:') > -1:
            #     result['date'] = u'考评年度'+header_title[header_title.find(u'年度:')+3:]
            #     print 'yes'


        # if(cmd_debug):
        #     cv2.imshow('view', header_image)
        #     cv2.waitKey(0)

        if(cmd_debug):
            print 'doc type----------------'
            print doc_type
            cv2.imshow('view', rotated)
            cv2.waitKey(0)

        result['type'] = doc_type

        answer_blocks = get_answer_blocks(blocks,grid,doc_type)
        buttom_bocks = get_bottom_blocks(blocks,doc_type,grid,iw,ih)
        right_blocks = get_right_blocks(blocks,doc_type,grid,iw,ih)

        if(cmd_debug):
            print('answer blocks',len(answer_blocks))
            print('buttom blocks',len(buttom_bocks))
            print('right blocks',len(right_blocks))

            cv2.drawContours(rotated, answer_blocks, -1, (0, 0, 255), 2)
            cv2.imshow('view', rotated)
            cv2.waitKey(0)

        (x,y,w,h) = cv2.boundingRect(grid)

        

        if doc_type == 1 :
            # 内容名称 b0-b1 | r0-r1
            # 指标名称 b2-b4 | r0 r1 r2 r3 r4 r5 r6
            # 指标分数 b5-b14 | r0 r1 r3 r4 r5 r6 r7 r8 r9 r10
            for i in range(10):
                x1 = cv2.boundingRect(buttom_bocks[2])[0]+10
                y1 = cv2.boundingRect(right_blocks[i])[1]-10
                x2 = cv2.boundingRect(buttom_bocks[4])[0]+cv2.boundingRect(buttom_bocks[4])[2]-10
                y2 = cv2.boundingRect(right_blocks[i])[1]+cv2.boundingRect(right_blocks[i])[3]+10

                # if y1 > y+h or y2 > y+h:
                #     continue

                # OCR 不识别 指标名称

                # cv2.rectangle(rotated,(x1,y1),(x2,y2),(0,0,255),2)

                # tmp = crop_image(rotated,[x1,x2,y1,y2])

                # tmp_file = "ocr_tmp_"+time.strftime("%Y%m%d%H%M%S",time.localtime())+'_'+(''.join(random.choice('abcdefghijklmn') for _ in range(5)))+'.jpg'
                # cv2.imwrite(tmp_file, tmp)
                # measure_name = ocr.ocr(tmp_file).replace(' ', '')
                # os.remove(tmp_file)

                # if(cmd_debug):
                #     print measure_name

                point = 0
                for j in range(0,10):
                    b = get_block_by_row_and_col(answer_blocks,right_blocks[i],buttom_bocks[5+j],doc_type,grid)
                    if b is not None:
                        # answer_blocks.remove(b)
                        # cv2.drawContours(rotated, [b], -1, (0, 255, 0), 2)
                        point = 10-j
                        break
                # if point==0:
                #     point = 10

                # if(cmd_debug):
                #     cv2.imshow('view', rotated)
                #     cv2.waitKey(0)
                
                if(cmd_debug):
                    print ('point : ',point)

                if not result.has_key('datas'):
                    result['datas'] = []

                result['datas'].append({'index':i+1,'name':'','point':point})

            block_a = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[5],doc_type)
            block_b = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[6],doc_type)
            block_c = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[7],doc_type)
            block_d = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[8],doc_type)
            block_e = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[9],doc_type)

            result['entity'] = ''
            if block_a is not None:
                result['entity'] = 'A票'

                # cv2.drawContours(rotated, [block_a], -1, (0, 255, 0), 2)

            if block_b is not None:
                result['entity'] = 'B票'

                # cv2.drawContours(rotated, [block_b], -1, (0, 255, 0), 2)
            if block_c is not None:
                result['entity'] = 'C票'

                # cv2.drawContours(rotated, [block_c], -1, (0, 255, 0), 2)
            if block_d is not None:
                result['entity'] = 'D票'

                # cv2.drawContours(rotated, [block_d], -1, (0, 255, 0), 2)
            if block_e is not None:
                result['entity'] = 'E票'

                # cv2.drawContours(rotated, [block_e], -1, (0, 255, 0), 2)

            # if(cmd_debug):
            #     cv2.imshow('view', rotated)
            #     cv2.waitKey(0)

            if(cmd_debug):
                print result['entity']

        if doc_type == 2 :
            # 内容名称 b0 | r2-r10 ...
            # 指标名称 b1-b2 | r2-r4 r5-r7 r8-r10 r11-r13 ...
            # 指标分数 b3-b6 b7-b10 ..... | r2-r4 r5-r7 r8-r10 r11-r13 ...

            for j in range(4):
                # delete by yelong 增加人员考评票的页数，用于人员的识别，不再使用汉字识别
                # # 姓名 b3-b6 b7-b10 b11-b14 b15-b18 b19-b22 b23-26 b27-b30 b31-b34 r0-r1
                # x1 = cv2.boundingRect(buttom_bocks[3+j*4])[0]+10
                # y1 = cv2.boundingRect(right_blocks[0])[1]+10
                # x2 = cv2.boundingRect(buttom_bocks[6+j*4])[0]+cv2.boundingRect(buttom_bocks[6+j*4])[2]-10
                # y2 = cv2.boundingRect(right_blocks[1])[1]+cv2.boundingRect(right_blocks[1])[3]-10
                
                # # cv2.rectangle(rotated,(x1,y1),(x2,y2),(0,0,255),2)

                # tmp = crop_image(rotated,[x1,x2,y1,y2])

                # tmp_file = "ocr_tmp_"+time.strftime("%Y%m%d%H%M%S",time.localtime())+'_'+(''.join(random.choice('abcdefghijklmn') for _ in range(5)))+'.jpg'
                # cv2.imwrite(tmp_file, tmp)
                # manager_name = ocr.ocr(tmp_file).replace(' ', '')
                # os.remove(tmp_file)

                # if (manager_name==None or len(manager_name)==0):
                #     continue

                # if(cmd_debug):
                #     print ('manager----------')
                #     print (manager_name)
                manager_name = ''

                if not result.has_key('datas'):
                    result['datas'] = []

                manager_result = { 'index':j+1,'name':manager_name,'datas':[] }

                for i in range(11):
                    x1 = cv2.boundingRect(buttom_bocks[1])[0]-10
                    y1 = cv2.boundingRect(right_blocks[2+(i*3)])[1]-10
                    x2 = cv2.boundingRect(buttom_bocks[2])[0]+cv2.boundingRect(buttom_bocks[2])[2]-10
                    y2 = cv2.boundingRect(right_blocks[2+(i*3)+2])[1]+cv2.boundingRect(right_blocks[2+(i*3)+2])[3]

                    # if y1 > y+h or y2 > y+h:
                    #     continue

                    # OCR 不识别 指标名称

                    # cv2.rectangle(rotated,(x1,y1),(x2,y2),(0,0,255),2)

                    # tmp = crop_image(rotated,[x1,x2,y1,y2])

                    # tmp_file = "ocr_tmp_"+time.strftime("%Y%m%d%H%M%S",time.localtime())+'_'+(''.join(random.choice('abcdefghijklmn') for _ in range(5)))+'.jpg'
                    # cv2.imwrite(tmp_file, tmp)
                    # tname = ocr.ocr(tmp_file).replace(' ', '')
                    # os.remove(tmp_file)

                    # if(cmd_debug):
                    #     cv2.imshow('view', rotated)
                    #     cv2.waitKey(0)
                    
                    # if(cmd_debug):
                    #     print tname

                    # 指标分数 b3-b6 b7-b10 ..... | r2-r3 r4-r5 r6-r7 r8-r9
                    point = 0
                    found = False
                    for r in range(0,3):
                        for c in range(0,4):

                            if cmd_debug:
                                print('R',2+i*3+r,'B',3+j*4+c, i, j)
                            b = get_block_by_row_and_col(answer_blocks,right_blocks[2+i*3+r],buttom_bocks[3+j*4+c],doc_type,grid)
                            if b is not None:
                                found = True
                                # area = cv2.contourArea(b)
                                # print('R',2+i*3+r,'B',3+j*4+c, i, j, area)
                                # answer_blocks.remove(b)
                                # cv2.drawContours(rotated, [b], -1, (0, 255, 0), 2)
                                if(r==0):
                                    if(c==0):
                                        point = 10
                                        #found = False
                                    if(c==1):
                                        found = False
                                    if(c==2):
                                        found = False
                                    if(c==3):
                                        point = 9
                                        #found = False
                                else:
                                    point = 12-(r*4+c)
                            if found:
                                break
                        if found:
                            break
                    
                    # if point==0:
                    #     point = 10

                    if(cmd_debug):
                        print(j,i,'point',point)

                    # if(cmd_debug):
                    #     cv2.imshow('view', rotated)
                    #     cv2.waitKey(0)

                    manager_result['datas'].append({ 'index':i+1,'name':'','point':point })
                
                result['datas'].append(manager_result)

            block_a = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[6],doc_type)
            block_b = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[7],doc_type)
            block_c = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[8],doc_type)
            block_d = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[9],doc_type)
            block_e = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[10],doc_type)
            result['entity'] = ''
            if block_a is not None:
                result['entity'] = 'A票'

                # cv2.drawContours(rotated, [block_a], -1, (0, 255, 0), 2)

            if block_b is not None:
                result['entity'] = 'B票'

                # cv2.drawContours(rotated, [block_b], -1, (0, 255, 0), 2)

            if block_c is not None:
                result['entity'] = 'C票'

                # cv2.drawContours(rotated, [block_c], -1, (0, 255, 0), 2)

            if block_d is not None:
                result['entity'] = 'D票'

                # cv2.drawContours(rotated, [block_d], -1, (0, 255, 0), 2)

            if block_e is not None:
                result['entity'] = 'E票'

                # cv2.drawContours(rotated, [block_e], -1, (0, 255, 0), 2)

            if(cmd_debug):
                print result['entity']

            # add by yelong 增加人员考评票的页数，用于人员的识别
            block_p1 = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[11],doc_type)
            block_p2 = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[12],doc_type)
            block_p3 = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[13],doc_type)
            block_p4 = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[14],doc_type)
            block_p5 = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[15],doc_type)
            block_p6 = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[16],doc_type)
            block_p7 = get_type_by_row_and_col(blocks,right_blocks[len(right_blocks)-1-1],buttom_bocks[17],doc_type)
            result['pageno'] = None
            if block_p1 is not None:
                result['pageno'] = 0
            if block_p2 is not None:
                result['pageno'] = 1
            if block_p3 is not None:
                result['pageno'] = 2
            if block_p4 is not None:
                result['pageno'] = 3
            if block_p5 is not None:
                result['pageno'] = 4
            if block_p6 is not None:
                result['pageno'] = 5
            if block_p7 is not None:
                result['pageno'] = 6

            # if(cmd_debug):
            #     cv2.imshow('view', rotated)
            #     cv2.waitKey(0)
        return { 'file':filepath,'data':result }
    else:
        print filepath + 'file not exist'

        return None

def get_all_files(paths,cmd_debug=False):
    all_files = []
    for filepath in paths:
        if(os.path.exists(filepath)):
            if os.path.isdir(filepath):
                files = os.listdir(filepath)
                for file in files:
                    fileAbsPath = os.path.join(filepath, file)
                    if os.path.isdir(fileAbsPath):
                        all_files.extend(get_all_files(fileAbsPath,cmd_debug))
                    else:
                        if re.search('\.jpg$',fileAbsPath):
                            all_files.append(fileAbsPath)
                        elif re.search('\.jpeg$',fileAbsPath):
                            all_files.append(fileAbsPath)
                        elif re.search('\.png$',fileAbsPath):
                            all_files.append(fileAbsPath)
            else:
                all_files.append(filepath)
    return all_files

def scan(paths,cmd_debug=False):
    all_files = get_all_files(paths,cmd_debug)
    result = []
    for file_path in all_files:
        data = ident(file_path,cmd_debug)
        print(file_path,'scan result:')
        print(data)
        result.append(data)
    return result

def main(argv):
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    cmd_debug = True
    
    if(cmd_debug):
        cv2.namedWindow("view", cv2.WINDOW_NORMAL)

    # filepath=unicode(argv[0],'utf8')
    
    result = ident(argv[0],cmd_debug)

    print result

    if(cmd_debug):
        cv2.destroyAllWindows()

    print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

if __name__ == '__main__':
    main(sys.argv[1:])
# -*-coding: utf-8 -*-
"""
    @Author : PKing
    @E-mail : 390737991@qq.com
    @Date   : 2022-12-31 11:37:30
    @Brief  :
"""
import os
import cv2
import time
from tqdm import tqdm
from multiprocessing import Pool
import numpy as np
from pybaseutils import file_utils, image_utils, base64_utils, time_utils
from pybaseutils.base_audio import audio_utils
import socket
import cv2
import numpy
from time import sleep


def get_boxes_up(xyxy, scale=(), cut=0.3):
    """获得boxes上半部分"""
    dxyxy = []
    for i in range(len(xyxy)):
        xmin, ymin, xmax, ymax = xyxy[i]
        w, h = (xmax - xmin), (ymax - ymin)
        ymax = max(ymin + h * cut, ymin + w)
        dxyxy.append([xmin, ymin, xmax, ymax])
    dxyxy = np.asarray(dxyxy)
    if scale: dxyxy = image_utils.extend_xyxy(dxyxy, scale=scale)
    return dxyxy


if __name__ == '__main__':
    image_file = "/home/PKing/nasdata/dataset/tmp/smoking/sample.png"
    boxes = [[47, 52, 255, 420]]
    boxes = np.asarray(boxes)
    image = cv2.imread(image_file)
    up = get_boxes_up(xyxy=boxes, scale=(), cut=0.3)
    image = image_utils.draw_image_boxes(image, boxes=boxes, color=(255, 0, 0))
    image = image_utils.draw_image_boxes(image, boxes=up, color=(0, 255, 0))
    image_utils.cv_show_image("image", image)

# -*-coding: utf-8 -*-
"""
    @Author : PKing
    @E-mail :
    @Date   : 2023-08-10 10:18:32
    @Brief  :
"""
import os
import numpy as np
from pybaseutils import image_utils, file_utils, color_utils
from pybaseutils.dataloader import base_coco


class CocoInstances(base_coco.CocoDataset):
    def __init__(self, anno_file, image_dir="", class_name=[], transform=None,
                 target_transform=None, use_rgb=False,
                 shuffle=False, check=False, **kwargs):
        """
        initialize COCO api for instance annotations
        :param anno_file:
        :param image_dir:
        :param class_name:
        :param transform:
        :param target_transform:
        :param use_rgb:
        :param shuffle:
        :param check:
        :param kwargs:
        """
        super(CocoInstances, self).__init__(anno_file, image_dir=image_dir, class_name=class_name, transform=transform,
                                            target_transform=target_transform, use_rgb=use_rgb,
                                            shuffle=shuffle, check=check, **kwargs)

    def __getitem__(self, index):
        """
        :param vis:
        :return: 
        """
        image_id = self.image_ids[index]
        anns_info, file_info = self.get_object_annotations(image_id)
        image, width, height = self.get_object_image(file_info)
        boxes, labels, mask, segs = self.get_object_instance(anns_info, h=height, w=width, decode=True)
        data = {"segs": segs, "mask": mask, "image": image, "boxes": boxes, "label": labels, "image_ids": image_id,
                "annotations": anns_info, "file_info": file_info}
        return data


def show_target_image(image, mask, boxes, labels, class_name=[], thickness=2, fontScale=1.0):
    mask = np.asarray(mask, np.uint8)
    color_image, color_mask = color_utils.decode_color_image_mask(image, mask)
    color_image = image_utils.draw_image_bboxes_labels(color_image, boxes, labels, class_name=class_name,
                                                       thickness=thickness, fontScale=fontScale)
    vis_image = image_utils.image_hstack([image, mask, color_image, color_mask])
    image_utils.cv_show_image("image", vis_image)


if __name__ == "__main__":
    class_name = {'person': 1, 'bicycle': 0, 'car': 2, 'motorcycle': 3, 'airplane': 4, 'bus': 5, 'train': 6, 'truck': 7,
                  'boat': 8, 'traffic light': 9, 'fire hydrant': 10, 'stop sign': 11, 'parking meter': 12, 'bench': 13,
                  'bird': 14, 'cat': 15, 'dog': 16, 'horse': 17, 'sheep': 18, 'cow': 19, 'elephant': 20,
                  'bear': 21, 'zebra': 22, 'giraffe': 23, 'backpack': 24, 'umbrella': 25, 'handbag': 26, 'tie': 27,
                  'suitcase': 28, 'frisbee': 29, 'skis': 30, 'snowboard': 31, 'sports ball': 32, 'kite': 33,
                  'baseball bat': 34, 'baseball glove': 35, 'skateboard': 36, 'surfboard': 37, 'tennis racket': 38,
                  'bottle': 39, 'wine glass': 40, 'cup': 41, 'fork': 42, 'knife': 43, 'spoon': 44, 'bowl': 45,
                  'banana': 46, 'apple': 47, 'sandwich': 48, 'orange': 49, 'broccoli': 50, 'carrot': 51, 'hot dog': 52,
                  'pizza': 53, 'donut': 54, 'cake': 55, 'chair': 56, 'couch': 57, 'potted plant': 58, 'bed': 59,
                  'dining table': 60, 'toilet': 61, 'tv': 62, 'laptop': 63, 'mouse': 64, 'remote': 65, 'keyboard': 66,
                  'cell phone': 67, 'microwave': 68, 'oven': 69, 'toaster': 70, 'sink': 71, 'refrigerator': 72,
                  'book': 73, 'clock': 74, 'vase': 75, 'scissors': 76, 'teddy bear': 77, 'hair drier': 78,
                  'toothbrush': 79}
    # class_name = []
    class_name = ["BG", 'person', 'car']
    # class_name = {'bb': "bk", "person": "unique"}
    # 测试COCO数据集
    coco_root = "/home/PKing/nasdata/dataset/face_person/COCO/"
    image_dir = coco_root + 'val2017/images'
    # anno_file = coco_root + 'annotations/person_keypoints_val2017.json'
    anno_file = coco_root + 'annotations/instances_val2017.json'

    anno_file = "/media/PKing/新加卷1/SDK/base-utils/data/coco/coco_ins.json"
    image_dir = "/media/PKing/新加卷1/SDK/base-utils/data/coco/JPEGImages"
    class_name = None
    #
    # anno_file = "/media/PKing/新加卷1/SDK/base-utils/data/coco/coco_ins.json"
    # anno_file = "/home/PKing/nasdata/dataset/tmp/hand-pose/FreiHAND/training/coco_kps.json"
    # image_dir = "/home/PKing/nasdata/dataset/tmp/hand-pose/FreiHAND/training/rgb"
    # class_name = None
    dataset = CocoInstances(anno_file, image_dir=image_dir, class_name=class_name)
    class_name = dataset.class_name
    for i in range(len(dataset)):
        data = dataset.__getitem__(i)
        image, boxes, labels, mask = data['image'], data["boxes"], data["label"], data["mask"]
        print("i={},image_ids={}".format(i, data["image_ids"]))
        # dataset.showAnns(image, data['annotations'])
        show_target_image(image, mask, boxes, labels, class_name=class_name)

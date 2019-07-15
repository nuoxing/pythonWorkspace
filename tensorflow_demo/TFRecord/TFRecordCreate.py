# -*- coding: utf-8 -*-
import os
import tensorflow as tf
from PIL import Image
import numpy as np

def _int64_feature(value):
    return tf.train.Feature(int64_list = tf.train.Int64List(value = [value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list = tf.train.BytesList(value = [value]))

def createTFRecord(cwd,classes,targetDir):
    writer = tf.python_io.TFRecordWriter(targetDir)  # 输出成tfrecord文件
    for index, name in enumerate(classes):
        class_path = cwd + name + '//'
        for img_name in os.listdir(class_path):
            print("正在执行类别为："+name)

            img_path = class_path + img_name  # 每个图片的地址
            img = Image.open(img_path)
            # img = img.resize((208, 208))
            img_raw = img.tobytes()  # 将图片转化为二进制格式
            example = tf.train.Example(features=tf.train.Features(feature={
                "label": _int64_feature(int(name)),
                "img_raw": _bytes_feature(img_raw),
                "width": _int64_feature(img.size[0]),
                "height": _int64_feature(img.size[1]),
            }))
            writer.write(example.SerializeToString())  # 序列化为字符串
    writer.close()

if __name__ == '__main__':
    cwd = "E:/pythonWorkspace.git/trunk/tensorflow_demo/mnist_digits_images/"
    classes = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}  # 预先自己定义的类别
    targetDir = 'minist6.tfrecords'
    createTFRecord(cwd,classes,targetDir)

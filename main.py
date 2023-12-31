# -*- coding: utf-8 -*-
import os

import cv2
import base64
import tempfile
from fastapi import FastAPI, Body


def template_match(tpl, target):
    th, tw = tpl.shape[:2]
    result = cv2.matchTemplate(target, tpl, cv2.TM_CCOEFF_NORMED)
    # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    tl = max_loc
    br = (tl[0] + tw, tl[1] + th)
    # 绘制矩形边框，将匹配区域标注出来
    # target：目标图像
    # tl：矩形定点
    # br：矩形的宽高
    # (0,0,255)：矩形边框颜色
    # 1：矩形边框大小
    cv2.rectangle(target, tl, br, (0, 0, 255), 2)
    return tl[0]


class SlideCrack(object):
    def __init__(self, gap, bg):
        """
        init code
        :param gap: 缺口图片
        :param bg: 背景图片
        """
        self.gap = gap
        self.bg = bg

    @staticmethod
    def clear_white(img):
        # 清除图片的空白区域，这里主要清除滑块的空白
        img = cv2.imread(img)
        rows, cols, channel = img.shape
        min_x = 255
        min_y = 255
        max_x = 0
        max_y = 0
        for x in range(1, rows):
            for y in range(1, cols):
                t = set(img[x, y])
                if len(t) >= 2:
                    if x <= min_x:
                        min_x = x
                    elif x >= max_x:
                        max_x = x

                    if y <= min_y:
                        min_y = y
                    elif y >= max_y:
                        max_y = y
        img1 = img[min_x:max_x, min_y: max_y]
        return img1

    @staticmethod
    def image_edge_detection(img):
        edges = cv2.Canny(img, 100, 200)
        return edges

    def discern(self):
        img1 = self.clear_white(self.gap)
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        slide = self.image_edge_detection(img1)

        back = cv2.imread(self.bg, 0)
        back = self.image_edge_detection(back)

        slide_pic = cv2.cvtColor(slide, cv2.COLOR_GRAY2RGB)
        back_pic = cv2.cvtColor(back, cv2.COLOR_GRAY2RGB)
        x = template_match(slide_pic, back_pic)
        # 输出横坐标, 即 滑块在图片上的位置
        return x


app = FastAPI()


@app.get("/")
async def index():
    return {"code": 0, "msg": '欢迎使用酷曦科技滑块API'}


@app.post("/slider")
def slider(json_data: dict = Body(...)):
    # 处理滑块请求路由

    # 从json数据中获取滑块图片
    image1 = convert_base64_to_file(json_data.get("sliderimage"))
    # 从json数据中获取背景图片
    image2 = convert_base64_to_file(json_data.get("bgimage"))

    # 创建滑块识别对象
    sc = SlideCrack(image1, image2)
    # 识别滑块的尺寸
    size = sc.discern()

    # 删除临时文件
    os.remove(image1)
    os.remove(image2)

    # 返回识别结果
    return {'code': 0, 'msg': '识别成功', 'data': {size}}


def convert_base64_to_file(base64_string) -> str:
    # 将base64字符串解码为二进制数据
    binary_data = base64.b64decode(base64_string)

    # 创建一个临时文件对象
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    # 写入二进制数据到文件
    temp_file.write(binary_data)

    # 获取文件路径
    file_path = temp_file.name

    # 关闭文件
    temp_file.close()

    return file_path

#encoding: UTF-8
#!/usr/bin/env python2
import cv2  # 导入OpenCV库，用于图像处理
import os  # 导入os库，用于文件和目录操作
import numpy as np  # 导入NumPy库，用于数值计算
import time  # 导入time库，用于时间操作
# import rospy  # 注释掉的ROS库
from pymycobot.mycobot import MyCobot  # 导入MyCobot库，用于控制机械臂
from opencv_yolo import yolo  # 导入YOLO库，用于目标检测
from VideoCapture import FastVideoCapture  # 导入快速视频捕获类
import math  # 导入数学库
from GrabParams import grabParams  # 导入抓取参数
import basic  # 导入基本操作模块
import argparse  # 导入argparse库，用于解析命令行参数

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='manual to this script')  # 创建解析器
parser.add_argument("--debug", type=bool, default="True")  # 添加debug参数
args = parser.parse_args()  # 解析参数

# 从抓取参数中获取偏移量
y_bias = grabParams.y_bias  # y轴偏移量
x_bias = grabParams.x_bias  # x轴偏移量
height_bias = grabParams.height_bias  # 高度偏移量

IMG_SIZE = grabParams.IMG_SIZE  # 图像尺寸

cap_num = grabParams.cap_num  # 摄像头编号2

# 是否显示图像和等待按键
debug = grabParams.debug  # 调试模式

coords = grabParams.coords_ready  # 准备好的坐标
done = grabParams.done  # 是否完成标志

# 定义检测标记类
class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()  # 调用父类构造函数

        # 初始化机械臂
        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)  # 创建MyCobot实例
        self.mc.power_on()  # 打开机械臂电源

        self.yolo = yolo()  # 初始化YOLO对象

        # 选择放置方块的位置
        self.color = 0  # 初始化颜色
        # 用于计算摄像头裁剪参数的变量
        self.x1 = self.x2 = self.y1 = self.y2 = 0        
        # 设置颜色的HSV范围
        self.HSV = {
            "yellow": [np.array([20, 43, 46]), np.array([26, 255, 255])],  # 黄色范围
            "red": [np.array([0, 43, 46]), np.array([10, 255, 255])],  # 红色范围
            "green": [np.array([50, 43, 46]), np.array([65, 255, 255])],  # 绿色范围
            "blue": [np.array([95,70 ,30]), np.array([110, 255, 205])],  # 蓝色范围
            "purple": [np.array([125, 43, 46]), np.array([155, 255, 255])],  # 紫色范围
        }
        # 用于计算方块与机械臂之间坐标的变量
        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0
        # 方块相对于机械臂的坐标
        self.c_x, self.c_y = IMG_SIZE/2, IMG_SIZE/2  # 图像中心点
        # 像素与实际值的比例
        self.ratio = grabParams.ratio  # 比例因子

    # 抓取动作
    def move(self, x, y):
        global height_bias, done  # 使用全局变量
        coords_target = [coords[0]+int(x), coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]  # 目标坐标
        basic.move_to_target_coords(coords_target, grabParams.GRAB_MOVE_SPEED)  # 移动到目标坐标

        basic.grap(True)  # 抓取动作

        angles = [0, 0, 0, 0, 0, 0]  # 机械臂角度
        self.mc.send_angles(angles,30)  # 发送角度指令
        time.sleep(3)  # 等待3秒

        done = True  # 设置完成标志
        print("Done")  # 打印完成信息
        self.mc.set_color(0,255,0)  # 设置机械臂颜色为绿色，表示空闲

    # 初始化机械臂
    def init_mycobot(self): 
        angles = [0, 0, 0, 0, 0, 0]  # 初始角度
        self.mc.send_angles(angles,30)  # 发送角度指令
        basic.grap(False)  # 松开抓取器      
        time.sleep(1)  # 等待1秒         
        basic.move_to_target_coords(coords,grabParams.GRAB_MOVE_SPEED)  # 移动到初始坐标

    # 获取目标位置
    def get_position(self, x, y):
        wx = wy = 0  # 初始化实际坐标
        if grabParams.grab_direct == "front":  # 如果抓取方向是前方
            wx = (self.c_y - y) * self.ratio  # 计算x坐标
            wy = (self.c_x - x) * self.ratio  # 计算y坐标
        elif grabParams.grab_direct == "right":  # 如果抓取方向是右侧
            wx = (self.c_x - x) * self.ratio  # 计算x坐标
            wy = (y - self.c_y) * self.ratio  # 计算y坐标
        return wx, wy  # 返回实际坐标

    # 转换图像帧
    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (IMG_SIZE, IMG_SIZE))  # 调整图像大小
        return frame  # 返回调整后的图像

    # 检测方块颜色
    def color_detect(self, img, mycolor):
        # 设置颜色HSV排列
        x = y = 0  # 初始化坐标
        # 只检测红色
        item = self.HSV[mycolor]  # 获取红色的HSV范围
        redLower = np.array(item[0])  # 下限
        redUpper = np.array(item[1])  # 上限
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 转换为HSV颜色空间
        mask = cv2.inRange(hsv, item[0], item[1])  # 生成掩膜
        erosion = cv2.erode(mask, np.ones((1, 1), np.uint8), iterations=2)  # 腐蚀操作
        dilation = cv2.dilate(erosion, np.ones((1, 1), np.uint8), iterations=2)  # 膨胀操作
        target = cv2.bitwise_and(img, img, mask=dilation)  # 按位与操作
        ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)  # 二值化
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 查找轮廓

        if len(contours) > 0:  # 如果找到轮廓
            boxes = [
                box
                for box in [cv2.boundingRect(c) for c in contours]
                if 110 < min(box[2], box[3]) and max(box[2], box[3]) < 170
            ]
            print(boxes)  # 打印检测到的框
            if boxes:
                for box in boxes:
                    x, y, w, h = box
                c = max(contours, key=cv2.contourArea)  # 找到最大轮廓
                x, y, w, h = cv2.boundingRect(c)  # 获取矩形框
                print(x, y, w, h)  # 打印矩形框信息
                cv2.rectangle(img, (x, y), (x+w, y+h), (153, 153, 0), 2)  # 绘制矩形框
                x, y = (x*2+w)/2, (y*2+h)/2  # 计算中心点
                self.color = 0  # 设置颜色为红色

        if abs(x) + abs(y) > 0:
            return x, y  # 返回坐标
        else:
            return None  # 未检测到目标

    def run(self):
        self.mc.set_color(0,0,255)  # 设置机械臂颜色为蓝色，表示忙碌
        self.init_mycobot()  # 初始化机械臂

    def show_image(self, img):
        print(args.debug)  # 打印调试信息
        if debug and args.debug:  # 如果调试模式开启
            cv2.imshow("figure", img)  # 显示图像
            cv2.waitKey(50)  # 等待50毫秒

if __name__ == "__main__":
    detect = Detect_marker()  # 创建检测标记对象
    detect.run()  # 运行检测

    cap = FastVideoCapture(cap_num)  # 创建视频捕获对象
    time.sleep(0.5)  # 等待0.5秒

    init_num = 0  # 初始化计数器
    nparams = 0  # 初始化参数
    num = 0  # 初始化计数
    miss = 0  # 初始化丢失计数
    while cv2.waitKey(1) < 0 and not done:  # 循环直到按下键或完成
        frame = cap.read()  # 读取视频帧

        frame = detect.transform_frame(frame)  # 转换图像帧

        detect_result = detect.color_detect(frame,"red")  # 检测颜色
        detect.show_image(frame)  # 显示图像
        if detect_result is None:            
            continue  # 如果未检测到，继续下一帧
        else:            
            x, y = detect_result  # 获取检测结果
            real_x, real_y = detect.get_position(x, y)  # 计算实际坐标
            coords_now = basic.get_coords()  # 获取当前坐标
            if len(coords_now) == 6:
                coords = coords_now  # 更新坐标
            detect.move(real_x + x_bias, real_y + y_bias)  # 移动机械臂
            cap.close()  # 关闭视频捕获
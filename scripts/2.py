#encoding: UTF-8
#!/usr/bin/env python2
import time  # 导入时间模块
from tast2 import Detect_marker  # 从tast2.py中导入Detect_marker类
from VideoCapture import FastVideoCapture  # 导入视频捕获类
from GrabParams import grabParams  # 导入抓取参数
import basic  # 导入基本操作模块

def main():
    detect = Detect_marker()  # 创建检测标记对象
    detect.run()  # 初始化机械臂
    cap = FastVideoCapture(grabParams.cap_num)  # 创建视频捕获对象
    time.sleep(0.5)  # 等待摄像头初始化

    # 第一次夹取红色物块
    while True:
        frame = cap.read()  # 读取视频帧
        frame = detect.transform_frame(frame)  # 转换图像帧
        detect_result = detect.color_detect(frame, "red")  # 检测红色物块
        detect.show_image(frame)  # 显示图像
        if detect_result is not None:  # 如果检测到红色物块
            x, y = detect_result  # 获取检测结果
            real_x, real_y = detect.get_position(x, y)  # 计算实际坐标
            coords_now = basic.get_coords()  # 获取当前机械臂坐标
            if len(coords_now) == 6:
                coords = coords_now  # 更新坐标
            detect.move(real_x + grabParams.x_bias, real_y + grabParams.y_bias)  # 移动机械臂夹取
            break  # 退出循环
    time.sleep(5)  # 等待5秒
    detect.init_mycobot()  # 丢弃物块
    while True:
        frame = cap.read()  # 读取视频帧
        frame = detect.transform_frame(frame)  # 转换图像帧
        detect_result = detect.color_detect(frame, "blue")  # 检测蓝色物块
        detect.show_image(frame)  # 显示图像
        if detect_result is not None:  # 如果检测到蓝色物块
            x, y = detect_result  # 获取检测结果
            real_x, real_y = detect.get_position(x, y)  # 计算实际坐标
            coords_now = basic.get_coords()  # 获取当前机械臂坐标
            if len(coords_now) == 6:
                coords = coords_now  # 更新坐标
            detect.move(real_x + grabParams.x_bias, real_y + grabParams.y_bias)  # 移动机械臂夹取
            break  # 退出循环
    time.sleep(5)  # 等待5秒
    detect.init_mycobot()  # 丢弃物块
    cap.close()  # 关闭视频捕获
    print("任务完成！")

if __name__ == "__main__":
    main()
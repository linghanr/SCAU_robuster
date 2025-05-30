from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams


mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
mc.set_color(0,0,255)#blue, arm is busy   

coords = grabParams.coords_ready
mc.send_coords(coords,15,0) #把手臂移动到准备好的坐标，该坐标是相机坐标系下的坐标
time.sleep(6)

mc.set_color(0,255,0)#green, arm is free


from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams
import basic
import time
from pymycobot.mycobot import MyCobot
import math
import rospy
from geometry_msgs.msg import Twist

def pose(a=203.6,b=-56.4,c=240.9,d=-178.34,e=2.93,f=-133.7):
    mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

    mc.set_color(0,0,255)#blue, arm is busy

    coords = [a,b,c,d,e,f]
    basic.move_to_target_coords(coords, 20)


    mc.set_color(0, 255, 0)  # green, arm is free
def release():
    basic.release_all_servos()



def main():
    pose(a=203.6,b=-56.4,c=240.9,d=-178.34,e=2.93,f=-133.7)
    print("123")
    time.sleep(2)
    release()
    mc.set_color(0,255,0)#green, arm is free

main()

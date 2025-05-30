#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	ratio = 0.21529956
	
	# increase x_bias to move front, or decrease x_bias to move back
	x_bias =-5
	# increase y_bias to move left, or decrease y_bias to move right
	y_bias = 47-5
	#               	 (+x)front
	#                 	  ^
	#				 	  :
	#				  	  :
	#                 	  :
	# (+y)< ..............o..............(-y)right
	#					  :
	#					  :
	#					  :
	#					  :
	#					 (-x)

	# increase height_bias to move higher, or decrease height_bias to move lower
	height_bias = 150	

	grab_direct = "front"
	coords_ready = [190, -25, 245, -175, 0, -134] #准备好的坐标

	# grab_direct = "right"
	# if grab_direct == "right":
	# 	y_bias = -5
	# 	x_bias = 40
	# 	coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	
	GRAB_MOVE_SPEED = 20

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()


# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0]
# Embedded file name: /home/robuster/beetle_ai/scripts/VideoCapture.py
# Compiled at: 2022-06-27 20:47:35
import cv2, Queue, threading, time
from GrabParams import grabParams
import os

class FastVideoCapture(object):

    def __init__(self, num):
        print('FastVideoCapture __init__: ')
        self.done = False
        self.cap = cv2.VideoCapture("/dev/armvideo") # , cv2.CAP_V4L2
        self.q = Queue.Queue()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()
        self.__init_flag = True

    def _reader(self):
        while not self.done:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except Queue.Empty:
                    pass

            self.q.put(frame)

    def read(self):
        return self.q.get()

    def getHeight(self):
        return self.cap.get(4)

    def getWidth(self):
        return self.cap.get(3)

    def close(self):
        self.done = True

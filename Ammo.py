import threading
import numpy as np
from PIL import ImageGrab
import cv2
import win32api
import win32con
import time


class Ammo(threading.Thread):
    def __init__(self):
        super(Ammo, self).__init__()
        self._stop_event = threading.Event()

        self.ammo_lower = np.array([79, 158, 169], np.uint8)
        self.ammo_upper = np.array([99, 178, 249], np.uint8)
        self.rio_ammo = [530, 130, 760, 370]
        self.ammo = np.array(ImageGrab.grab(bbox=self.rio_ammo))
        self.ammo = cv2.cvtColor(self.ammo, cv2.COLOR_BGR2HSV)
        self.mask_ammo = cv2.inRange(self.ammo, self.ammo_lower, self.ammo_upper)
        self.ammo_contours, _ = cv2.findContours(self.mask_ammo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            self.ammo = np.array(ImageGrab.grab(bbox=self.rio_ammo))
            self.ammo = cv2.cvtColor(self.ammo, cv2.COLOR_BGR2HSV)
            self.mask_ammo = cv2.inRange(self.ammo, self.ammo_lower, self.ammo_upper)
            self.ammo_contours, _ = cv2.findContours(self.mask_ammo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(self.ammo_contours) == 0:  # if out of ammo reload
                win32api.keybd_event(0x20, 0, 0, 0)  # 0x20 is hex for the space key
                time.sleep(0.25)
                win32api.keybd_event(0x20, 0, win32con.KEYEVENTF_KEYUP, 0)
            cv2.waitKey(1)
            cv2.imshow("ammo", self.mask_ammo)

import threading
import numpy as np
from PIL import ImageGrab
import cv2
import win32api
import win32con
import time


class Aimbot(threading.Thread):
    def __init__(self, ):
        super(Aimbot, self).__init__()
        self._stop_event = threading.Event()

        # this is where the game is located on your screen (or should be)
        self.rio_game = [640, 500, 1140, 650]

        # creating upper and lower boundary's used it the mask
        self.enemy_lower = np.array([0, 0, 0], np.uint8)
        self.enemy_upper = np.array([10, 10, 40], np.uint8)

        # this is a blur filter that takes away the edges
        self.kernel = np.ones((5, 5), "uint8")

        # take a screenshot and convert it to RGB
        self.game = np.array(ImageGrab.grab(bbox=self.rio_game))
        self.game = cv2.cvtColor(self.game, cv2.COLOR_BGR2RGB)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def click(self, x, y):  # function clicks on the given x and y
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    def run(self):
        while not self.stopped():
            e1 = cv2.getTickCount()  # only used to get the time

            # same as in the constructor
            self.game = np.array(ImageGrab.grab(bbox=self.rio_game))
            self.game = cv2.cvtColor(self.game, cv2.COLOR_BGR2RGB)

            # create the mask
            mask_game = cv2.dilate(cv2.inRange(self.game, self.enemy_lower, self.enemy_upper), self.kernel)

            # uncomment below to see how the mask looks like
            #cv2.imshow("mask", mask_game)

            # retrieve all contours found within the mask
            contours, _ = cv2.findContours(mask_game, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if contours:  # shoot all black stuff
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if 10 < area < 600:
                        x, y, w, h = cv2.boundingRect(contour)
                        x += (15 + 640)  # adjust coords first value is to center in on the head second is bc of rio
                        y += (2 + 500)
                        self.click(x, y)
            else:  # if there is no black stuff you might as well reload
                win32api.keybd_event(0x20, 0, 0, 0)  # 0x20 is hex for the space key
                time.sleep(0.25)
                win32api.keybd_event(0x20, 0, win32con.KEYEVENTF_KEYUP, 0)

            cv2.waitKey(10)  # wait a few ticks (lowest value is 1)

            e2 = cv2.getTickCount()  # some time stuff
            t = (e2 - e1) / cv2.getTickFrequency()
            print("It took Aimbot ", t, "sec to loop")

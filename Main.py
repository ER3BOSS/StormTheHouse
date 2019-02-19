import numpy as np
# External
import win32api
import threading
# Classes
from Ammo import Ammo
from Aimbot import Aimbot


def main():
    ammo_thread = Ammo()
    ammo_thread.start()

    aim_thread = Aimbot()
    aim_thread.start()

    mouse_x, mouse_y = win32api.GetCursorPos()

    while 610 < mouse_x:
        mouse_x, mouse_y = win32api.GetCursorPos()

    print("cursor out of bounds -> stopping ...")

    ammo_thread.stop()
    aim_thread.stop()

if __name__ == "__main__": main()
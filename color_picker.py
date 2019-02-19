import cv2
import numpy as np
from PIL import ImageGrab

'''

    # This is a standalone program I used to get the color ranges for the masks

'''


rio = [640, 500, 1070, 690]

cap = cv2.VideoCapture("outpy.avi")
cap.set(3, 1280)
cap.set(4, 1024)
cap.set(15, 0.1)

# image_hsv = None   # global ;(
# pixel = (20,60,80) # some stupid default

# mouse callback function
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]

        #you might want to adjust the ranges(+-10, etc):
        upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        u_string = np.array2string(upper)
        u_string = u_string.replace("  ", " ")
        u_string = u_string.replace(" ", ", ")
        u_string = u_string.replace("[, ", "[")
        lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        l_string = np.array2string(lower)
        l_string = l_string.replace("  ", " ")
        l_string = l_string.replace(" ", ", ")
        l_string = l_string.replace("[, ", "[")
        print(l_string, u_string)

        image_mask = cv2.inRange(image_hsv,lower,upper)
        cv2.imshow("mask",image_mask)

while True:
    e1 = cv2.getTickCount()

    global image_hsv, pixel # so we can use it in mouse callback

    image_src = np.array(ImageGrab.grab(bbox=rio))# cv2.imread(sys.argv[1])  # pick.py my.png
    image_hsv = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image_hsv, cv2.COLOR_RGB2HSV)

    if image_src is None:
        print ("the image read is None............")
        break
    # cv2.imshow("bgr",image_src)

    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv', pick_color)

    # now click into the hsv img , and look at values:
    cv2.imshow("hsv",image_src)

    e2 = cv2.getTickCount()
    t = (e2 - e1) / cv2.getTickFrequency()


    if cv2.waitKey(200) == ord('q'):  # shutdown (increase waitkey value to slow down replay speed)
        cv2.destroyAllWindows()
        break

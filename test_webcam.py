#
# inspired by: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
#
import cv2
import numpy as np

#
# config
#

# if you have an external webcam check if you need to use 0 or 1 (I think depends the way you start)
# 0 is the first in the list of discovered cam
# in my case Mac OS list the USB webcam as the first, so it is 0, the internal is 1
SOURCE = 0
WINDOW_NAME = "test"

# code of some keys used
ESC_KEY = 27
R_KEY = 114

#
# functions
#

# check if ESC or R_KEY key has been pressed
# the window showing the image must have focus
def check_key(key_pressed, key_to_check):
    
    v_rit = False

    if key_pressed%256 == key_to_check:
        v_rit = True

    return v_rit

def get_frame_info(cam):
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    print()
    print("Camera info:")
    print(f"Frame width: {width}")
    print(f"Frame height: {height}")
    print()

    return height, width

# show how to add a red BB
# at the middle of the image
def add_rectangle(frame, half_side):
    # Red color in BGR (image is already in BGR)
    # consider that cv2 works in BGR not RGB
    color = (0, 0, 255)
  
    # Line thickness of 2 px
    thickness = 2

    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)

    # get the CENTER
    xc = int(width/2)
    yc = int(height/2)

    start_point = (xc - half_side, yc - half_side)
    end_point = (xc + half_side, yc + half_side)
  
    # Using cv2.rectangle() method
    # Draw a rectangle with red line borders of thickness of 2 px
    frame = cv2.rectangle(frame, start_point, end_point, color, thickness)  
    
    return frame

#
# end functions
#

#
# Main
#
cam = cv2.VideoCapture(SOURCE)
cv2.namedWindow(WINDOW_NAME)

if not cam.isOpened():
    print("Error, cannot open camera !!!")
    exit()

# get info
height, width = get_frame_info(cam)

img_counter = 0
flag_rec = False

#
# Loop
#
while True:
    # Capture frame-by-frame
    ret, frame = cam.read()
    
    # frame is a numpy array containing the image
    # shape is (height, width, 3)

    if not ret:
        print("failed to grab frame")
        break
    
    img_counter += 1

    # show how to add a RED BB on screen (toggle with r key)
    if flag_rec:
        # the BB is centered and has side = 2*half_side
        frame = add_rectangle(frame, half_side = 200)

    # show the image captured
    cv2.imshow(WINDOW_NAME, frame)

    # test if need to close or to add a red BB
    k = cv2.waitKey(1)

    if k > 0:
        # print(f"key pressed is: {k}")
    
        # test if ESC pressed -> close
        if check_key(k, ESC_KEY):
            # ESC pressed
            print("Escape hit, closing...")
            print()
            break

        # if R_KEY -> flag to add/remove BB on screen
        if check_key(k, R_KEY):
           flag_rec = not flag_rec 

# closing
cam.release()
cv2.destroyAllWindows()
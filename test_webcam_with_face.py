#
# inspired by: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
#
import cv2
import numpy as np
# the conda env is face_recognition
# added dlib and face_recognition to the conda env
import face_recognition

#
# config
#

# if you have an external webcam check if you need to use 0 or 1 (depends the way you start the Mac)
# 0 is the first in the list of discovered cam
# in my case Mac OS list the USB webcam as the first, so it is 0, the internal is 1
SOURCE = 0
WINDOW_NAME = "test"

# code of some keyboard keys used
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
def add_rectangle(frame, start_point, end_point):
    # Red color in BGR (image is already in BGR)
    # consider that cv2 works in BGR not RGB
    color = (0, 0, 255)
  
    # Line thickness of 2 px
    thickness = 2
  
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
# cv2.namedWindow(WINDOW_NAME)

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

    if flag_rec:
        # ok wants a rectangle around the face

        # resize to speed up (after will multiply by 4) the face recognition process
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # convert to RGB, that is used by face_recognition
        small_frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # apply face detection
        face_locs = face_recognition.face_locations(small_frame_rgb, 
            # less accurate but faster without this parm.
            model="cnn")

        if len(face_locs) > 0:
            # found face
            top, right, bottom, left = face_locs[0]

            # return back to initial size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # add a RED BB on original image (toggle with r key)
            frame = add_rectangle(frame, (left, top), (right, bottom))

    # show the image captured (eventually with BB)
    cv2.imshow(WINDOW_NAME, frame)

    # test if need to close or to add/remove a red BB
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
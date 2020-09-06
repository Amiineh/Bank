# From Python
# It requires OpenCV installed for Python
import sys
import os
import math
from sys import platform
import argparse
import time

class OP():
    def __init__(self):
        self.phone_detected = False
        self.label = {
            'nose': 0,
            'head': 0,
            'neck': 1,
            'r_shoulder': 2,
            'r_elbow': 3,
            'r_hand': 4,
            'l_shoulder': 5,
            'l_elbow': 6,
            'l_hand': 7,
            'r_hip': 8,
            'r_knee': 9,
            'r_foot': 10,
            'l_hip': 11,
            'l_knee': 12,
            'l_foot': 13,
            'r_eye': 14,
            'l_eye': 15,
            'r_ear': 16,
            'l_ear': 17,
        }

        try:
            # Import Openpose (Windows/Ubuntu/OSX)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            try:
                # Windows Import
                if platform == "win32":
                    # Change these variables to point to the correct folder (Release/x64 etc.)
                    sys.path.append('/usr/local/python/openpose/Release');
                    os.environ['PATH'] = os.environ[
                                             'PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
                    import pyopenpose as op
                else:
                    # Change these variables to point to the correct folder (Release/x64 etc.)
                    # sys.path.append('../../python');
                    # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                    sys.path.append('/usr/local/python')
                    from openpose import pyopenpose as op
            except ImportError as e:
                print(
                    'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
                raise e

            # Flags
            parser = argparse.ArgumentParser()
            # parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
            op_dir = "/home/amineh/Documents/Dance/openpose"
            parser.add_argument("--image_path", default=op_dir + "/examples/media/COCO_val2014_000000000192.jpg",
                                help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
            args = parser.parse_known_args()

            # Custom Params (refer to include/openpose/flags.hpp for more parameters)
            params = dict()
            params["model_folder"] = op_dir + "/models/"
            params["model_pose"] = "COCO"
            params["camera"] = 0
            params["part_candidates"] = 1
            params["number_people_max"] = 1
            # params["process_real_time"] = 1

            # Add others in path?
            for i in range(0, len(args[1])):
                curr_item = args[1][i]
                if i != len(args[1]) - 1:
                    next_item = args[1][i + 1]
                else:
                    next_item = "1"
                if "--" in curr_item and "--" in next_item:
                    key = curr_item.replace('-', '')
                    if key not in params:  params[key] = "1"
                elif "--" in curr_item and "--" not in next_item:
                    key = curr_item.replace('-', '')
                    if key not in params: params[key] = next_item

            # Construct it from system arguments
            # op.init_argv(args[1])
            # oppython = op.OpenposePython()

            # Starting OpenPose
            self.opWrapper = op.WrapperPython()
            self.opWrapper.configure(params)
            self.opWrapper.start()

            self.datum = op.Datum()

        except Exception as e:
            print(e)
            sys.exit(-1)

    def estimate(self, img):
        self.datum.cvInputData = img
        self.opWrapper.emplaceAndPop([self.datum])
        self.detect_phone()

        return self.datum.cvOutputData, self.datum.poseCandidates, self.phone_detected


    def detect_phone(self):
        if not self.eyes_visibe():
            self.phone_detected = False
        elif self.hand_near_ear():
            print("def phone ", time.time())
            self.phone_detected = True
        else:
            self.phone_detected = False

    def eyes_visibe(self):
        def get_keypoint(l):
            points = self.datum.poseCandidates
            return points[self.label[l]]

        l_eye = get_keypoint('l_eye')
        r_eye = get_keypoint('r_eye')
        if len(l_eye) == 0 or len(r_eye) == 0:
            return False
        return True

    def hand_near_ear(self, percision=0.1):

        def get_keypoint(l):
            points = self.datum.poseCandidates
            return points[self.label[l]]

        def distance(point_a, point_b):
            if len(point_a) == 0 or len(point_b) == 0:
                return -1

            xa, ya, pa = point_a[0]     # todo: clean unpack
            xb, yb, pb = point_b[0]
            if pa * pb < percision:
                return -2
            return math.sqrt((xa-xb)**2 + (ya-yb)**2)

        # if dist(hand, ear) < dist(ear, ear) -> phone
        l_hand_ear_dist = distance(get_keypoint('l_hand'), get_keypoint('l_ear'))
        r_hand_ear_dist = distance(get_keypoint('r_hand'), get_keypoint('r_ear'))
        ear_ear_dist = distance(get_keypoint('l_ear'), get_keypoint('r_ear'))

        if ear_ear_dist > 0:
            if (l_hand_ear_dist > 0 and l_hand_ear_dist < ear_ear_dist) or \
                    (r_hand_ear_dist > 0 and r_hand_ear_dist < ear_ear_dist):
                print('l_hand_ear_dist: ', l_hand_ear_dist)
                print('r_hand_ear_dist:', r_hand_ear_dist)
                print('ear_ear_dist:', ear_ear_dist)
                return True

        return False
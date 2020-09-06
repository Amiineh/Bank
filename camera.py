import cv2
from op import OP

ds_factor = 0.6


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self, op):
        success, image = self.video.read()
        cv_output_data, pose_candidates = op.estimate(image)
        ret, jpeg = cv2.imencode('.jpg', cv_output_data)
        return jpeg.tobytes()

    def get_output(self, op):
        success, image = self.video.read()
        cv_output_data, pose_candidates, phone_detected = op.estimate(image)
        return cv_output_data, pose_candidates, phone_detected
import io
import picamera
import numpy as np
import time
import cv2

class VideoCamera(object):
    def __init__(self):
        # Create the in-memory stream
        self.stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)
            camera.capture(self.stream, format='jpeg')
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        pass
        # self.video.release()
    
    def get_frame(self):
        # success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        # ret, jpeg = cv2.imencode('.jpg', image)
        data = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

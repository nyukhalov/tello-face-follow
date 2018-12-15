import tellopy
import cv2
import av
import sys
import numpy as np
import traceback
import time
from face_detector import FaceDetector
from renderer import Renderer

class DroneState(object):
    def __init__(self):
        self.battery = None # battery percentage 0..1
        self.speed = None # drone's speed
        self.wifi = None # wifi connection level 0..1

drone_state = DroneState()

def main():
    face_detector = FaceDetector()
    renderer = Renderer()

    try:
        container = av.open('video/ball_tracking_example.mp4')
        num_skip_frames = 300
        while True:
            for frame in container.decode(video=0):
                if num_skip_frames > 0:
                    num_skip_frames = num_skip_frames - 1
                    continue
                start_time = time.time()

                image = np.array(frame.to_image())
                image = cv2.resize(image, (432, 240))
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                face = face_detector.detect(image)
                renderer.render(image, drone_state, face)

                if face is not None:
                    image_cx = image.shape[1] // 2
                    image_cy = image.shape[0] // 2
                    offset_x = face.cx - image_cx
                    offset_y = face.cy - image_cy
                    print(offset_x, offset_y)

                cv2.imshow('Original', image)
                cv2.waitKey(1)

                time_base = max(1/60, frame.time_base)
                processing_time = time.time() - start_time
                num_skip_frames = int(processing_time/time_base)
                print('Video steam %d FPS, frame time base=%f' % (1/frame.time_base, frame.time_base))
                print('Processing FPS=%d, time=%f, skip frames=%d' % (1/processing_time, processing_time, num_skip_frames))

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

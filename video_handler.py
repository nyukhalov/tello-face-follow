#!/usr/bin/env python
import tellopy
import cv2
import av
import sys
import numpy as np
import traceback
import time
from face_detector import FaceDetector
from renderer import Renderer
from display import Cv2Display2D, PygameDisplay
from model import DroneState

drone_state = DroneState()

def main():
    W = 432
    H = 240
    image_cx = W // 2
    image_cy = H // 2    

    face_detector = FaceDetector()
    renderer = Renderer()
    #display = Cv2Display2D()
    display = PygameDisplay(W, H)

    try:
        container = av.open('video/ball_tracking_example.mp4')
        num_skip_frames = 0
        while True:
            for frame in container.decode(video=0):
                if num_skip_frames > 0:
                    num_skip_frames = num_skip_frames - 1
                    continue
                start_time = time.monotonic()

                image = np.array(frame.to_image())
                image = cv2.resize(image, (W,H))

                face = face_detector.detect(image)
                renderer.render(image, drone_state, face)

                if face is not None:
                    offset_x = face.cx - image_cx
                    offset_y = face.cy - image_cy
                    print(offset_x, offset_y)

                display.paint(image)

                time_base = max(1/60, frame.time_base)
                processing_time = time.monotonic() - start_time
                num_skip_frames = int(processing_time/time_base)
                print('Video steam %d FPS, frame time base=%f' % (1/frame.time_base, frame.time_base))
                print('Processing FPS=%d, time=%f ms, skip frames=%d' % (1/processing_time, 1000 * processing_time, num_skip_frames))

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

    finally:
        display.dispose()

if __name__ == '__main__':
    main()

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
from pid import PID
from controller import Controller

drone_state = DroneState()

def flight_data_handler(event, sender, data):
    global drone_state
    text = str(data)
    tokens = text.split('|')
    params_dict = {}
    for token in tokens:
        param_value = token.split(':')
        param = param_value[0].strip()
        value = param_value[1].strip()
        params_dict[param] = value
    battery = int(params_dict['BAT']) / 100.0
    wifi = int(params_dict['WIFI']) / 100.0
    speed = int(params_dict['SPD'])
    drone_state.battery = battery
    drone_state.wifi = wifi
    drone_state.speed = speed

def main():
    # original frame size is (720, 960)
    W = 320
    H = 240
    image_cx = W // 2
    image_cy = H // 2    

    num_skip_frames = 300

    drone = tellopy.Tello()
    controller = Controller(drone, image_cx, image_cy)
    face_detector = FaceDetector()
    renderer = Renderer()
    display = PygameDisplay(W, H)

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        drone.subscribe(drone.EVENT_FLIGHT_DATA, flight_data_handler)
        container = av.open(drone.get_video_stream())

        drone.takeoff()

        while True:
            for frame in container.decode(video=0):
                if num_skip_frames > 0:
                    num_skip_frames = num_skip_frames - 1
                    continue
                start_time = time.time()
                image = np.array(frame.to_image())
                image = cv2.resize(image, (W,H))

                face = face_detector.detect(image)
                controller.control(face)
                renderer.render(image, drone_state, face)
                display.paint(image)

                time_base = max(1.0/60, frame.time_base)
                processing_time = time.time() - start_time
                num_skip_frames = int(processing_time/time_base)
                #print('Video steam %d FPS, frame time base=%f' % (1/frame.time_base, frame.time_base))
                #print('Processing FPS=%d, time=%f ms, skip frames=%d' % (1/processing_time, 1000 * processing_time, num_skip_frames))
                
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

    finally:
        drone.land()
        drone.quit()
        display.dispose()

if __name__ == '__main__':
    main()

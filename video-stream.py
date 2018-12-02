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
    drone = tellopy.Tello()
    face_detector = FaceDetector()
    renderer = Renderer()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        drone.subscribe(drone.EVENT_FLIGHT_DATA, flight_data_handler)

        container = av.open(drone.get_video_stream())
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if frame_skip > 0:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()

                image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                faces = face_detector.detect(image)
                renderer.render(image, drone_state, faces)

                cv2.imshow('Original', image)
                cv2.waitKey(1)
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                processing_time = time.time() - start_time
                frame_skip = int(processing_time/time_base)
                print('Processing time=%f, skip frames=%d' % (processing_time, frame_skip))

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

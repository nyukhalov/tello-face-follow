import tellopy
import cv2
import av
import sys
import numpy as np
import traceback
import time
from face_detector import FaceDetector

def main():
    drone = tellopy.Tello()
    face_detector = FaceDetector()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        frame_skip = 500
        while True:
            for frame in container.decode(video=0):
                if frame_skip > 0:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                faces = face_detector.detect(image)
                for (x,y,w,h) in faces:
                    cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)
                cv2.imshow('Original', image)
                cv2.waitKey(1)
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                processing_time = time.time() - start_time
                frame_skip = int(processing_time/time_base)
                print(processing_time)
                print(frame_skip)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

import cv2

class FaceDetector(object):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('conf/haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            print('Face cascade configuration not found')
            raise Exception('Face cascade configuration not found')

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces



import cv2

class FaceDetector(object):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('conf/haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            print('Face cascade configuration not found')
            raise Exception('Face cascade configuration not found')

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        return faces



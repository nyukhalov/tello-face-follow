import cv2
from model import Face

class FaceDetector(object):
    def __init__(self, max_recovery=30):
        self.face_cascade = cv2.CascadeClassifier('conf/haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            print('Face cascade configuration not found')
            raise Exception('Face cascade configuration not found')
        self.last_face = None
        self.max_recovery = max_recovery
        self.num_recovery = 0

    def detect(self, image):
        """
        returns a Face object or None if a face does not found
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            if self.num_recovery >= self.max_recovery:
                self.last_face = None
                self.num_recovery = 0
            if self.last_face is not None:
                self.num_recovery = self.num_recovery + 1
            return self.last_face

        (x, y, w, h) = faces[0]
        face = Face(x, y, w, h)
        self.last_face = face
        self.num_recovery = 0
        return face



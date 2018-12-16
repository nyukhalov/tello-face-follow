import cv2

class Display2D(object):
    def __init__(self):
        pass

    # abstract
    def paint(self, img):
        pass

class Cv2Display2D(Display2D):
    def __init__(self, win_title='Main'):
        self.win_title = win_title

    def paint(self, img):
        cv2.imshow(self.win_title, img)
        cv2.waitKey(1)

class PygameDisplay(Display2D):
    def __init__(self):
        pass

    def paint(self, img):
        pass

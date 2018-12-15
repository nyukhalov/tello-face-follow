class Face(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cx = self.x + self.w // 2
        self.cy = self.y + self.h // 2


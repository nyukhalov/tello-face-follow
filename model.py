class Face(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cx = self.x + self.w // 2
        self.cy = self.y + self.h // 2

class DroneState(object):
    def __init__(self):
        self.battery = None # battery percentage 0..1
        self.speed = None # drone's speed
        self.wifi = None # wifi connection level 0..1
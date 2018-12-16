import cv2

class Renderer(object):
    def __init__(self):
        pass

    def render(self, image, drone_state, face):
        self.render_faces(image, face)

        stats = []
        stats.append(self.get_battery(drone_state))
        stats.append(self.get_wifi(drone_state))
        self.render_stats(image, stats)

    def render_faces(self, image, face):
        if face is not None:
            cv2.rectangle(image, (face.x,face.y), (face.x+face.w, face.y+face.h), (255,0,0), 2)
            cv2.circle(image, (face.cx, face.cy), 2, (0,255,0))

    def get_battery(self, drone_state):
        if drone_state.battery is None:
            return 'Battery: ???'
        else:
            return 'Battery: %0.2f' % drone_state.battery

    def get_wifi(self, drone_state):
        if drone_state.wifi is None:
            return 'WIFI: ???'
        else:
            return 'WIFI: %0.2f' % drone_state.wifi

    def render_stats(self, image, stats):
        for idx, stat in enumerate(stats):
            cv2.putText(image, stat, (0, 30 + idx*30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), lineType=30)



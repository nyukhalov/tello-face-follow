import cv2

class Renderer(object):
    def __init__(self):
        pass

    def render(self, image, drone_state, faces):
        self.render_faces(image, faces)

        stats = []
        stats.append(self.get_battery(drone_state))
        stats.append(self.get_wifi(drone_state))
        self.render_stats(image, stats)

    def render_faces(self, image, faces):
        for (x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)

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



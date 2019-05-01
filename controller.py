from pid import PID

target_obj_size = 45

class Controller(object):
    def __init__(self, drone, image_cx, image_cy):
        self.drone = drone
        self.image_cx = image_cx
        self.image_cy = image_cy
        self.h_pid = PID(0.1, 0.00001, 0.01)
        self.v_pid = PID(0.5, 0.00001, 0.01)
        self.dist_pid = PID(0.1, 0.00001, 0.01)

    def control(self, target):
        if target is not None:

            # distance
            dist_error = target_obj_size - target.w
            dist_control = self.dist_pid.control(dist_error)
            if dist_control >= 0:
                self.drone.forward(dist_control)
            else:
                self.drone.backward(abs(dist_control))

            # rotation
            offset_x = target.cx - self.image_cx
            h_control = self.h_pid.control(offset_x)
            if h_control >= 0:
                self.drone.clockwise(h_control)
            else:
                self.drone.counter_clockwise(abs(h_control))

            offset_y = target.cy - self.image_cy
            # v_control = self.v_pid.control(-offset_y)
            # if v_control >= 0:
            #    drone.up(v_control)
            # else:
            #    drone.down(abs(v_control))

            print("offset=(%d,%d), cur_size=%d, size_error=%d, h_control=%f" %
                  (offset_x, offset_y, target.w, dist_error, h_control))
        else:
            self.h_pid.reset()
            self.v_pid.reset()
            self.dist_pid.reset()
            self.drone.clockwise(0)
            self.drone.up(0)
            self.drone.forward(0)

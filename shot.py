import math
from collections import deque
#76
class Shot:
    def __init__(self, min_h, running_avg_length=10, running_avg_multiplier=0.7):
        self.theta = 0
        self.x0 = 0
        self.y0 = 0
        self.v00x = 0
        self.v00y = 0
        self.v0x = 0
        self.v0y = 0
        self.avg_v = 0
        self.avg_v0 = 0
        self.initialized = False
        self.min_h = min_h
        self.running_avg_length = running_avg_length
        self.running_avg_multiplier = running_avg_multiplier
        self.running_avg_buffer = deque(maxlen=running_avg_length)
        self.reset()

    def update(self, t, x, y):
        x *= .0020365
        y *= .0020365
        # print("pos: " + str(x) + ", " + str(y))
        avg_v_decreased = False
        if self.initialized:
            vx = (x - self.x0) / t
            vy = (y - self.y0) / t
            print("vel: " + str(vx) + ", " + str(vy))
            # print("vel: " + str(vx) + ", " + str(vy))
            v = math.sqrt(vx * vx + vy * vy)
            avg_v = self.get_avg_v(v)
            if avg_v < self.avg_v0:
                avg_v_decreased = True
            self.avg_v0 = avg_v
            self.v00x = self.v0x
            self.v00y = self.v0y
            self.v0x = vx
            self.v0y = vy
        else:
            self.initialized = True
        self.x0 = x
        self.y0 = y
        if avg_v_decreased and y >= self.min_h:
            return True
        return False

    def get_avg_v(self, v):
        self.running_avg_buffer.append(v)
        avg = 0
        denom = 0
        for i, j in zip(range(self.running_avg_length), range(self.running_avg_length - 1, -1, -1)):
            mult = self.running_avg_multiplier ** i
            avg += self.running_avg_buffer[j] * mult
            denom += mult
        return avg / denom

    def reset(self):
        self.theta = 0
        self.x0 = 0
        self.y0 = 0
        self.v00x = 0
        self.v00y = 0
        self.v0x = 0
        self.v0y = 0
        self.avg_v = 0
        self.avg_v0 = 0
        self.initialized = False
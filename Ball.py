from Constants import*

class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = abs(vy)
        self.r = BALL_D/2
    
    def updateVel(self, fps):
        self.vy += A_GRAV/fps/fps
        print("Vel of ball: " + str(self.vx) + ", " + str(self.vy))
    
    def updatePos(self, fps):
        self.x += self.vx
        self.y += self.vy

    def update(self, fps):
        self.updateVel(fps)
        self.updatePos(fps)
    

    
        
        
            

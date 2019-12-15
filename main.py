from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time as ti
from p5 import *
import Detector
import shot
from Ball import*
from Constants import*
from Rect import*





heightField = None
distField = None
ball = None

inHand = True
trackerX = 0
trackerY = 0
ppm = 0
fps = 20
started = False
startPos = []
settingUp = True
height = 850
width = 1440

currX = 0
currY = 0



def setup():
    global detector, vs, frame_rate, prev, shotDetector, ppm, cp5, heightField, distField, backboard, rim, courtFloor, rects
    size(width, height)

    detector = Detector.Detector()
    vs = VideoStream(src=0).start()
    shotDetector = shot.Shot(2.35)
    frame_rate = 20
    prev = 0
    ppm = height / 5  # pixels per meter
    backboard = Rect(width - BACKBOARD_WIDTH * ppm - 5, height - TOP_BACKBOARD * ppm, BACKBOARD_WIDTH * ppm,
                     BACKBOARD_HEIGHT * ppm)
    rim = Rect(width - BACKBOARD_WIDTH * ppm - 5 - HOOP_D * ppm, height - HOOP_HEIGHT * ppm, HOOP_D * ppm, 5)
    courtFloor = Rect(0, height - 10, width, 10)
    rects = [backboard, rim, courtFloor]

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def willBounce(ball, rects):
    for rect in rects: #each rect is a list of x,y,w,h
        if ball.x * ppm + ball.r *ppm >= rect[0] and ball.x * ppm - ball.r * ppm <= rect[0] + rect[2]:
            if ball.y *ppm + ball.r * ppm >= rect[1] and ball.y *ppm - ball.r *ppm <= rect[1] + rect[3]:
                bounce(rect)

def bounce(ball, rect):
    if ball.y *ppm >= rect[1] and ball.y *ppm <= rect[1] + rect[3]:
        ball.vx *= -COEF_REST
    else:
        ball.vy *= -COEF_REST

def drawRect(rectangle):
    rect((rectangle.x,rectangle.y), rectangle.w, rectangle.h)

def leaveHand(x,y,vx,vy):
    global ball
    ball = Ball(x,y,vx,vy)


def draw():
    global detector, prev, vs, shotDetector, started, height, width, ball, inHand, fps, currX, currY
    background(255)
    fill(0)
    stroke_weight(0)
    frame = vs.read()
    detector.process(vs, frame)

    fill(0)
    drawRect(backboard)
    fill(244, 140, 0)
    drawRect(rim)
    fill(224, 198, 112)
    drawRect(courtFloor)

    # free throw
    fill(0, 200, 0)
    r1 = Rect(width - FREETHROW_DIST * ppm - 5, height - 10, 5, 10)
    drawRect(r1)

    # top of key
    fill(0, 0, 200)
    r2 = Rect(width - TOP_KEY_DIST * ppm - 5, height - 10, 5, 10)
    drawRect(r2)


    # three point line
    fill(200, 0, 0)
    r3 = Rect(width - THREEPOINT_DIST * ppm - 5, height - 10, 5, 10)
    drawRect(r3)
    fill(255, 102, 0)
    print(detector.centerPoint)
    width2 = translate(detector.centerPoint[0], 0, 700, width // 2, 0)
    height2 = translate(detector.centerPoint[1], 0, 300, 0, height // 2)
    circle((width2 * 2, height2 * 2), 50)
    #
    # # ball - if in hand?
    # fill(0, 0, 0)
    # bHeight = 0
    # bDist = FREETHROW_DIST
    # if ball is not None:
    #     print(ball.x, ball.y)
    #     # print(ball.vx, ball.vy)

    # if inHand:
    #     print("INHAND******")
    #     print("xy: " + str(width - (bDist * ppm)) + ", " + str(height - bHeight * ppm - BALL_D / 2 * ppm - 10))
    #     if started and detector.centerPoint is not None:
    #         #circle((ball.x * ppm, height - ball.y * ppm), BALL_D * ppm)
    #         circle((translate(detector.centerPoint[0], 0, 600, width//2, 0), translate(detector.centerPoint[1], 0, 330, 0, height//2)), BALL_D * ppm)
    #         currX = translate(detector.centerPoint[0], 0, 600, width // 2, 0)
    #         currY = translate(detector.centerPoint[1], 0, 330, 0, height // 2)
    #     # else:
    #     #     circle((width - (bDist * ppm), (height - bHeight * ppm - BALL_D / 2 * ppm - 10)), BALL_D * ppm)
    # else:
    #
    #     print("***** OUT OF HAND")
    #     currX += ball.x * ppm
    #     currY += height-ball.y*ppm
    #     circle((currX, currY), BALL_D * ppm)
    #     ball.update(fps)
        # willBounce(ball, rects)
        #circle((400, 400), 50)

    # if not inHand:
    #     ball.update(fps)
    #     willBounce(ball, rects)

    # print("started: " + str(started))
    # # if started:
    # #     print("STARTED ENTERED")
    # # time_elapsed = ti.time() - prev
    #
    # # if time_elapsed > 1. / frame_rate:
    # #     prev = ti.time()
    # frame = vs.read()
    # detector.process(vs, frame)
    # fill(255, 102, 0)
    # width = translate(detector.centerPoint[0], 0, 600, width//2, 0)
    # height = translate(detector.centerPoint[1], 0, 330, 0, height//2)
    # circle((width*2, height*2), 50)
            # rWidth = frame.shape[0] - detector.centerPoint[0]
            # rHeight = frame.shape[1] - detector.centerPoint[1]
            # if shotDetector.update(time_elapsed, rWidth, rHeight):
            #     if started:
            #         print("release vel: " + str(shotDetector.v00x) + ", " + str(shotDetector.v00y))
            #         leaveHand(shotDetector.x0, shotDetector.y0, shotDetector.v0x/fps, -shotDetector.v0y/fps)
            #         started = False
            #         inHand = False
            # else:
            #     print("coords: " + str(shotDetector.v00x) + ", " + str(shotDetector.v00y))




def key_pressed():
    global started, inHand, ball, shotDetector
    if str(key) == " ":
        started = True
    if str(key) == "r" or str(key) == "R":
        started = False
        inHand = True
        ball = None
        shotDetector.reset()



if __name__ == '__main__':
    run()

# -*- coding: utf-8 -*-
'''
Created on 25/05/2015

@author: david
'''

import cv2
import math

import numpy as np


class TrackedItem(object):
    
    def __init__(self, fileName, drawColor, frameSize):
        
        self._frameSize = frameSize
        self._trackWindow = (1, 1, self._frameSize[0]-2, self._frameSize[1]-2)                
        self._drawColor = drawColor
        
        sampleBGR = cv2.imread(fileName)
        #cv2.imshow(fileName, sampleBGR)
        
        sampleHSV = cv2.cvtColor(sampleBGR, cv2.COLOR_BGR2HSV)
        self._hist = cv2.calcHist([sampleHSV], [0], None, [180], [0, 180])        
        cv2.normalize(self._hist, self._hist, 0, 255, cv2.NORM_MINMAX)

        self._termCriteria = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        self._boxedPoints = None
        self._centerPoint = None
    
        
    def track(self, frameHSV, mask):        
        
        bp = cv2.calcBackProject([frameHSV],[0],self._hist,[0,180],1)
        bp = cv2.bitwise_and(bp,bp, mask=mask)
        itemPoints, self._trackWindow = cv2.CamShift(bp, self._trackWindow, self._termCriteria)
        
        if self._trackWindow[0] > 0 and self._trackWindow[1] > 0 \
            and self._trackWindow[2] > 1 and self._trackWindow[3] > 1:
            
            try:
                pts = cv2.cv.BoxPoints(itemPoints)
                self._boxedPoints = np.int0(pts)
            except:
                self._boxedPoints = None
        else:
            self._trackWindow = (1, 1, self._frameSize[0]-2, self._frameSize[1]-2)
            self._boxedPoints = None
        
        if self._boxedPoints != None:
            self._centerPoint = (self._trackWindow[0] + self._trackWindow[2]/2, self._trackWindow[1] + self._trackWindow[3]/2)
        else:
            self._centerPoint = None
        
            
    def draw(self, outputFrame):
        
        if self._boxedPoints != None:
            cv2.polylines(outputFrame,[self._boxedPoints],True, self._drawColor,4)
            cv2.line(outputFrame, tuple((np.array(self._centerPoint) + np.array((0, -2))).tolist()) \
                     , tuple((np.array(self._centerPoint) + np.array((0, 2))).tolist()), self._drawColor, 1)
            cv2.line(outputFrame, tuple((np.array(self._centerPoint) + np.array((-2, 0))).tolist()) \
                     , tuple((np.array(self._centerPoint) + np.array((2, 0))).tolist()), self._drawColor, 1)
    
    
    def isFound(self):
        
        return self._centerPoint != None
            
    
    def getCenter(self):
        
        return self._centerPoint
        

class TrackedDifference(object):
    
    def __init__(self, frameSize):
        
        self._eX  = 0
        self._eY  = 0
        self._eZ  = 0
        self._eAZ  = 0
        
        self._frameSize = frameSize
        
        
    def draw(self, outputFrame):
        
        text = "Errors: X = {0}; Y = {1}; Z = {2}; AZ = {3}".format(self._eX, self._eY, self._eZ, self._eAZ)
        cv2.putText(outputFrame, text, (4, self._frameSize[1] - 4), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 255))
        
    
    def getData(self):
        
        return [self._eX, self._eY, self._eZ, self._eAZ]
        

class VisualTracker(object):

    RES_PATH = "./drone/res"

    def __init__(self):
        
        self._cam = cv2.VideoCapture(0)
        
        self._cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        self._cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        
        camHeight = self._cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        camWidth = self._cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        
        self._frameSize = (int(camWidth), int(camHeight))
        
        self._distRefY = self._frameSize[1] / 2        
        
        #logging.debug("Capture size: {0}".format(frameSize))
    
        self._trackedItems = [
            TrackedItem(VisualTracker.RES_PATH + '/item1.png', (0, 255, 0), self._frameSize),   #green
            TrackedItem(VisualTracker.RES_PATH + '/item2.png', (0, 0, 255), self._frameSize),   #red                    
            TrackedItem(VisualTracker.RES_PATH + '/item3.png', (255, 0, 0), self._frameSize),   #blue
            TrackedItem(VisualTracker.RES_PATH + '/item4.png', (255, 255, 0), self._frameSize) #cyan
        ]
        
        refPointMargin = self._frameSize[1]/5
        self._refPoint = (self._frameSize[0] - refPointMargin, self._frameSize[1] - refPointMargin)
        
        
        #Video        
        #self._videoWriter = cv2.VideoWriter('/home/debian/output.avi',cv.CV_FOURCC('M','J','P','G'), 20.0, self._frameSize)
        self._videoWriter = open("/home/debian/output.vid", "w")

        

    @staticmethod
    def _distance(point1, point2):
        
        a = (point2[0] - point1[0])**2
        b = (point2[1] - point1[1])**2
        d = int(math.sqrt(a+b))
        
        return d
    
    
    def track(self):
    
        _, frame = self._cam.read()
        frame = cv2.flip(frame, 1)        
        frame = cv2.medianBlur(frame, 5)
        
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frameHSV, np.array([0, 50, 60]), np.array([180, 255, 255]))        
        
        output = frame        

        #Draw reference point
        cv2.circle(output, self._refPoint, 4, (0, 255, 255), 7)
        
        for trackedItem in self._trackedItems:
            
            trackedItem.track(frameHSV, mask)
            trackedItem.draw(output)
        
        difference = TrackedDifference(self._frameSize)
        
        if self._trackedItems[3].isFound():
            point3 = self._trackedItems[3].getCenter()        
            cv2.line(output, self._refPoint, point3, (0, 255, 255), 1)
            
            difference._eX = point3[0] - self._refPoint[0]
            difference._eZ = point3[1] - self._refPoint[1]
            
            if self._trackedItems[1].isFound():                                
                cv2.circle(output, point3, self._distRefY, (0, 255, 255), 1)
                point1 = self._trackedItems[1].getCenter()
                cv2.line(output, point3, point1, (0, 255, 255), 1)
                
                distanceY = VisualTracker._distance(point3, point1)
                difference._eY = distanceY - self._distRefY

                if self._trackedItems[2].isFound() and self._trackedItems[0].isFound():
                    point0 = self._trackedItems[0].getCenter()                    
                    point2 = self._trackedItems[2].getCenter()
                    cv2.line(output, point0, point2, (0, 255, 255), 1)
                    
                    distance1 = VisualTracker._distance(point1, point3)
                    cv2.circle(output, point2, distance1, (0, 255, 255), 1)
                    
                    distance2 = VisualTracker._distance(point0, point2)
                    difference._eAZ = distance2 - distance1
        
        #video
        difference.draw(output)
        self._videoWriter.write(output.tostring())

        #logging.debug(datetime.datetime.now())
        
        results = difference.getData()     
                
        return results

    
    def close(self):
        
        cv2.destroyAllWindows()
        self._cam.release()
        self._videoWriter.close()
        

    def stop(self):
        self.close()

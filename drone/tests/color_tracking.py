# -*- coding: utf-8 -*-

'''
Created on 18/05/2015

@author: david
'''
import cv2

from flight.stabilization.visual_tracking import VisualTracker


def main():
    
    tracker = VisualTracker()    
    
    done = False
    while(not done):
        
        output = tracker.track()                 

        cv2.imshow('tracking',output)            

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            done = True
    
    tracker.close()


if __name__ == '__main__':
    main()
    
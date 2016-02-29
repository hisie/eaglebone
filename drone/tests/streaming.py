# -*- coding: utf-8 -*-
'''
Created on 23/05/2015

@author: david
'''
import cv2
import sys
import time


def main():
    
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    
    #camHeight = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    #camWidth = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    
    #frameSize = (int(camWidth), int(camHeight))
    
    #print "Capture size: {0}".format(frameSize)    
    
    done=False
    while not done:
        
        _, frame = cap.read()
        
        frame = cv2.flip(frame, 1)
        #_, jpeg = cv2.imencode(".jpg", frame)
        
        sys.stdout.write( frame.tostring() )
        
        #cv2.imshow('cam',frame)                    
        
        '''
        key = cv2.waitKey(100) & 0xff
        if key == ord('q'):
            done = True
	    '''

    time.sleep(0.1)

    cv2.destroyAllWindows()
    cap.release()
    



if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-

'''
Created on 08/04/2015

@author: david
'''
from flight.driving.driver import Driver
from math import radians

controller = Driver()
controller.start()
controller.standBy()

done = False

try:
    while not done:
    
        command = raw_input("Insert command: ").strip().split()
        command0 = command[0].upper()
    
        if command0 == "QUIT": #Quit
            done = True
            
        elif command0 == "TH":
            
            if len(command) == 2:
                increment = float(command[1])
                controller.addThrottle(increment)
            else:
                print "Throttle: TH increment"
            
        elif command0 == "SH":
            
            if len(command) == 3:
                angle = radians(float(command[1]))
                controller.shift(angle, float(command[2]))
            else:
                print "Shift: SH degrees-angle inc-percentage"
                
        elif command0 == "SP":
            
            if len(command) == 2:
                increment = float(command[1])
                controller.spin(increment)
            else:
                print "Spin: SP inc-percentage"
                
        elif command0 == "SB":            
            controller.standBy()
            
        elif command0 == "ID":
            controller.idle()
            
        elif command0 == "HELP":
            print "Commands list:"
            print "\tQUIT: Stop and exit"
            print "\tTH: Throttle"
            print "\tSH: Shift"
            print "\tSP: Spin"
            print "\tSB: Stand-by"
            print "\tID: Idle"
            
        else:
            print "Unknown command"

#except Exception as ex:
#    print "Error: {0}".format(ex)
#    raise ex

finally:
    controller.stop()
    print "Goodbye!"

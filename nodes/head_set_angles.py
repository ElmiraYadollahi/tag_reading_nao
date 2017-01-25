# -*- encoding: UTF-8 -*-

import sys
from naoqi import ALProxy
import time

def main(robotIP):
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    motionProxy.setStiffnesses("Head", 1.0)

    # Example showing how to set angles, using a fraction of max speed
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [0, 0.4]
    fractionMaxSpeed  = 0.05
    motionProxy.setAngles(names, angles, fractionMaxSpeed)

    """names               = "HeadYaw"
    changes             = -0.5
    fractionMaxSpeed    = 0.05
    motionProxy.changeAngles(names, changes, fractionMaxSpeed)"""

    time.sleep(3.0)
    motionProxy.setStiffnesses("Head", 0.0)


if __name__ == "__main__":
    robotIp = "10.0.0.6"

    if len(sys.argv) <= 1:
        print "Usage python almotion_setangles.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
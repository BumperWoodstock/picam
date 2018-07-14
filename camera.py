import picamera
import picamera.array
import time


threshold = 10 #howmuch pixel changes
sensitivity = 100 #how many pixels change

def takeMotionImage(width,height):
    with picamera.PiCamera() as camera:
        time.sleep(2)
        camera.resolution = (width,height)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream,format='rgb')
            return stream.array

def scanMotion(width,height):
    motionfound = False

    data1 = takeMotionImage(width,height)

    while not motionfound:
        data2 = takeMotionImage(width,height)
        diffCount = 0;
        for w in range(0,width):
            for h in range(0,height):
                #iterate through all the pixels
                #figure out if any have changed
                diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]) )

                if diff > threshold:
                    diffCount += 1

                if diffCount > sensitivity:
                    break

        if diffCount > sensitivity:
            motionfound = True
        else:
            data1 = data2 #compare against the previous array

    return motionfound

def captureImage(fname):
    with picamera.PiCamera() as camera:
        time.sleep(2)
        camera.resolution = (1024, 768)
        camera.capture(fname)

def motionDetection():
    print ( "Scanning for Motion threshold = %i sensitivity = %i..." % (threshold,sensitivity) )
    while True:
        if scanMotion(224,160):
            print ("motion detected")
            fname = "/media/pi/PiStorage/PiCamera/image%s.jpg" % time.strftime("%Y%m%d-%H%M%S")
            print ("Writing Image to %s" % fname)
            captureImage(fname)


if __name__ =='__main__':
    try:
        motionDetection()
    finally:
        print ("Exiting Program")

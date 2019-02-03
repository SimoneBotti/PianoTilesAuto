import time
import pyautogui
from mss import mss
from PIL import Image
import numpy
import cv2
import imutils
import sys
import json
import os



def displayMultiplePic(im):
    cv2.imshow("OpenCV/Numpy normal", im)



def displayPicture(im):
    cv2.imshow("OpenCV/Numpy normal", im)
    cv2.waitKey(0)



def putMouseinPosition(x,y,height):
    startX=655
    startY=32
    offH = (height / 2) - 15
    pyautogui.moveTo(startX+x, startY+y+offH)
    print("Putted Mouse in X: "+str(startX+x)+" Y: "+str(startY+y)+" Position New: "+str(offH))

def putMouseinPosition(top,left,x,y):
    startX=left
    startY=top
    if (y < 30):
        y += 150
    if (y < 100):
        y += 100
    pyautogui.moveTo(startX+x, startY+y)
    print("Putted Mouse in X: "+str(startX+x)+" Y: "+str(startY+y))




def putMouseinPositionandClick(x,y,height):
    startX=655
    startY=32
    offH=(height/2)-15
    pyautogui.click(startX+x, startY+y+offH)
    print("Putted Mouse in X: "+str(startX+x)+" Y: "+str(startY+y)+" Position New: "+str(offH))


def putMouseinPositionandClick(top,left,x,y):
    startX=left
    startY=top
    if(y<30):
        y+=150
    if(y<100):
        y+=100
    pyautogui.click(startX+x, startY+y)
    print("Putted Mouse in X: "+str(startX+x)+" Y: "+str(startY+y))


#SORT CONTOURS BOTTOM TO TOP
def sort_contours(cnts, method="bottom-to-top"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


def openCVmultipleScreen(top,left,width,height,Rmin,Gmin,Bmin,Rmax,Gmax,Bmax):
    top=int(top)
    left=int(left)
    width=int(width)
    height=int(height)
    Rmin=int(Rmin)
    Gmin=int(Gmin)
    Bmin=int(Bmin)
    Rmax=int(Rmax)
    Gmax=int(Gmax)
    Bmax=int(Bmax)
    with mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}

      #  last_time = time.time()
      #  ti = time.time()
      #  print("Riconoscimento black square: " + str(ti - last_time))
        while "Screen capturing":
            try:
                im = sct.grab(monitor)
                image = cv2.cvtColor(numpy.array(im), cv2.COLOR_BGR2RGB)
                lower = numpy.array([Rmin, Gmin, Bmin])
                upper = numpy.array([Rmax, Gmax, Bmax])
                shapeMask = cv2.inRange(image, lower, upper)
                #displayMultiplePic(shapeMask)
                cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
                orig = image.copy()
                print("I found {} black shapes".format(len(cnts)))
                if(len(cnts)==0):
                    continue
                # Sorting the countours
                (cnts, boundingBoxes) = sort_contours(cnts)
                threshold_area = 10000
                # loop over the contours
                for c in cnts:
                    area = cv2.contourArea(c)
                    if area > threshold_area:
                        x, y, w, h = cv2.boundingRect(c)
                        M = cv2.moments(c)
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        # print("Contorno x: "+str(x)+" Y: "+str(y)+" Width: "+str(w)+" Height: "+str(h));
                        putMouseinPositionandClick(top,left,cX, cY)
                        #putMouseinPosition(top,left,cX,cY)
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break
            except KeyboardInterrupt:
                print("closing")
                sys.exit




#THIS FUNCTION CHECK EVERYTHING ONLY FOR THE FIRST FRAME

def openCV(top,left,width,height,Rmin,Gmin,Bmin,Rmax,Gmax,Bmax):
    top = int(top)
    left = int(left)
    width = int(width)
    height = int(height)
    Rmin = int(Rmin)
    Gmin = int(Gmin)
    Bmin = int(Bmin)
    Rmax = int(Rmax)
    Gmax = int(Gmax)
    Bmax = int(Bmax)
    with mss() as sct:
        monitor = {"top": 90, "left": 382, "width": 540, "height": 673}
        # Get raw pixels from the screen, save it to a Numpy array

        last_time = time.time()

        im = sct.grab(monitor)
        image = cv2.cvtColor(numpy.array(im), cv2.COLOR_BGR2RGB)
        lower = numpy.array([0, 0, 0])
        upper = numpy.array([70, 170, 250])
        shapeMask = cv2.inRange(image, lower, upper)
        displayPicture(shapeMask)
        ti=time.time()
        print("Riconoscimento black square: "+str(ti-last_time))
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        orig = image.copy()
        print("I found {} black shapes".format(len(cnts)))

        #Sorting the countours
        (cnts, boundingBoxes) = sort_contours(cnts)
        threshold_area = 1000
        # loop over the contours
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            area = cv2.contourArea(c)
            print("Area :"+str(area))
            if area>threshold_area:

                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print("Contorno x: "+str(x)+" Y: "+str(y)+" Width: "+str(w)+" Height: "+str(h));
                putMouseinPosition(cX,cY,h)
                cv2.drawContours(shapeMask, [c], 0, (50, 50, 50), 3)
                time.sleep(2)
            #cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            #cv2.imshow("Image", image)
            #cv2.waitKey(0)
        displayPicture(shapeMask)
        # find the contours in the mask



def moveMouseandClick(x,y):
    pyautogui.click(x, y)

def moveMouse(x,y):
    pyautogui.moveTo(x, y)


def getScreenSize():
    mon = input("Insert the number of the screen(in case of multiple montor)")
    width, height = pyautogui.size()
    print("Screen width:"+str(width)+" Height:"+str(height))


def getGameScreenDim():
    print("Put the mouse in the 4 corners of game screen (Top-Left,Top-Right,Bottom-Right,Bottom-Left) in that order" + os.linesep)
    fourPoints=[]
    for i in range(4):
        let = input("Press ENTER to capture mouse position" + os.linesep)
        fourPoints.append(pyautogui.position())
        positionStr = 'X: ' + str(fourPoints[i][0]).rjust(4) + ' Y: ' + str(fourPoints[i][1]).rjust(4)
        print(positionStr)
    return fourPoints

def generateFile():
    fourPoints=getGameScreenDim()
    width=fourPoints[1][0]-fourPoints[0][0]
    height=fourPoints[2][1]-fourPoints[0][1]
    print("Ho X:"+str(fourPoints[0][0]))
    f = open("Calib.txt", "w+")
    dataScreen = {}
    dataObj = {}
    dataScreen['top'] = str(fourPoints[0][1])
    dataScreen['left'] = str(fourPoints[0][0])
    dataScreen['width'] = str(width)
    dataScreen['height'] = str(height)
    dataObj['Rmin'] ='0'
    dataObj['Gmin'] = '0'
    dataObj['Bmin'] = '0'
    dataObj['Rmax'] = '70'
    dataObj['Gmax'] = '170'
    dataObj['Bmax'] = '250'

    json_data = json.dumps(dataScreen)
    json_data2 = json.dumps(dataObj)
    f.write('Game Screen:'+ os.linesep)
    f.write(json_data)
    f.write(os.linesep+'Color range to find:'+ os.linesep)
    f.write(json_data2)
    f.close()

def readFile():
    f=open('Calib.txt','r')
    c=0
    for line in f:
       if line[0]=='{':
            dataJson = json.loads(line)
            if(c==0):
                top=dataJson['top']
                left=dataJson['left']
                width=dataJson['width']
                height=dataJson['height']
                c+=1
            else:
                Rmin=dataJson['Rmin']
                Gmin = dataJson['Gmin']
                Bmin = dataJson['Bmin']
                Rmax = dataJson['Rmax']
                Gmax = dataJson['Gmax']
                Bmax = dataJson['Bmax']
    openCVmultipleScreen(top,left,width,height,Rmin,Gmin,Bmin,Rmax,Gmax,Bmax)
    #openCV(top, left, width, height, Rmin, Gmin, Bmin, Rmax, Gmax, Bmax)


def main():
    #openCVmultipleScreen()
    #generateFile()
    choice=int(input("0 To Exit"+os.linesep+"1 For select the screen"+os.linesep+"2 To Play"+os.linesep))
    while choice!=0:
        if(choice==1):
            print("Selected 1")
            #getScreenSize()
            generateFile()
            #getGameScreenDim()
            print(os.linesep)
        elif(choice==2):
            print("Selected 2")
            readFile()
            print(os.linesep)
        choice = int(input("0 To Exit" + os.linesep + "1 For select the screen" + os.linesep + "2 To Play" + os.linesep))
    #readFile()


if __name__== "__main__":
  main()

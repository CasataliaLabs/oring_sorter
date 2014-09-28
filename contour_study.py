import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import time as time
frame = plt.imread("oring_sample_2.jpg")
frameForDraw = frame * 1;
imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
k = 0
while not k == -1:
#~ for k in np.arange(0, len(contours)):
    cv2.drawContours(frameForDraw, contours, k, (255,0,0), 1)
    plt.imshow(frameForDraw)
    print 'contour number : ', k
    print "length of contours cell: ", len(contours[k])
    print "the contour: ", contours[k]
    print "hierachy is: ", hierarchy[0,k,:]
    k = raw_input('Enter to Continue: ')
    k = int(k)


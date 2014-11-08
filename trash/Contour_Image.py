__author__ = 'Midhun EM'
import cv2
import matplotlib.pyplot as plt
import numpy
import numpy as np
import matplotlib.cm as cm
import time as time
from v4l2_capture_class import CaptureFromCam
from matplotlib.figure import Figure



'''vidDevicePath = '/dev/video*'
if (not 'cap' in locals()): #| (cap.camLink == None):
	cap = CaptureFromCam(vidDevicePath)

if cap.camLink == None:
	cap = CaptureFromCam(vidDevicePath)
if cap.camLink == None:	
	print 'camera error'
	#~ exit()
	print 'test exit'
	sys.exit(0)'''
#~ frame = cap.read()
frame = plt.imread("Image3.jpg")
frameForDraw = frame * 1
imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
k = -1
figure1 = plt.figure(1)
axes1 = figure1.add_subplot(121)
axes1.set_title("Contour")
axes2 = figure1.add_subplot(122)
axes2.grid(True)
axes2.set_title("Graph Plot")
axes2.set_xlabel("Angle")
axes2.set_ylabel("Radius")


#~ Contour section 

k = -1
cv2.drawContours(frameForDraw, contours, k, (255,0,0), 1)
print "Number of contours is",len(contours)
print 'contour number : ', k
print "length of hierachy is: ", len(hierarchy[0])
print "hierarchy is",hierarchy
parent = hierarchy[0,:,3]
childOuter = parent == 0
IndexOfZeroParentOuter= np.where(childOuter == True)[0]
areaOfContourOuter = []
for itration in range(0,len(IndexOfZeroParentOuter)):
	areaOfContourOuter.append(cv2.contourArea(contours[IndexOfZeroParentOuter[itration]]))
areaOfContourMaxOuter = np.max(areaOfContourOuter)
indexOfAreaOfContourMaxOuter = areaOfContourOuter.index(areaOfContourMaxOuter)
print " indexOfAreaOfContourMax",IndexOfZeroParentOuter[indexOfAreaOfContourMaxOuter]


childInner = parent == IndexOfZeroParentOuter[indexOfAreaOfContourMaxOuter]
IndexOfZeroParentInner= np.where(childInner == True)[0]
areaOfContourInner = []
for itration in range(0,len(IndexOfZeroParentInner)):
	areaOfContourInner.append(cv2.contourArea(contours[IndexOfZeroParentInner[itration]]))
areaOfContourMaxInner = np.max(areaOfContourInner)
indexOfAreaOfContourMaxInner= areaOfContourInner.index(areaOfContourMaxInner)
print " indexOfAreaOfContourMin",IndexOfZeroParentInner[indexOfAreaOfContourMaxInner]

cnt_OringOuter = contours[IndexOfZeroParentOuter[indexOfAreaOfContourMaxOuter ]]
cnt_OringInner = contours[IndexOfZeroParentInner[indexOfAreaOfContourMaxInner ]]
cv2.drawContours(thresh, contours, IndexOfZeroParentOuter[indexOfAreaOfContourMaxOuter] , (255,0,0), 0)
cv2.drawContours(thresh, contours, IndexOfZeroParentInner[indexOfAreaOfContourMaxInner], (255,0,0), 1)
axes1.imshow(thresh,cmap = cm.Greys) 
print "area for outer ring is : {} area for inner ring is : {}".format(cv2.contourArea(contours[IndexOfZeroParentOuter[indexOfAreaOfContourMaxOuter]]),cv2.contourArea(contours[IndexOfZeroParentInner[indexOfAreaOfContourMaxInner]])) 
print "Shape is",thresh.shape
xOuter = cnt_OringOuter[:,:,0]
xInner = cnt_OringInner[:,:,0]
x_OringOuter = xOuter[:,0]
x_OringInner = xInner[:,0]
yOuter = cnt_OringOuter[:,:,1]
yInner = cnt_OringInner[:,:,1]
y_OringOuter = yOuter[:,0]
y_OringInner = yInner[:,0]
Momnt_Oring = cv2.moments(cnt_OringOuter)
cx_Oring = int(Momnt_Oring['m10']/Momnt_Oring['m00'])
cy_Oring = int(Momnt_Oring['m01']/Momnt_Oring['m00'])

rad_Oring_Outer = ((x_OringOuter-cx_Oring)**2)+((y_OringOuter-cy_Oring)**2)
rad_Oring_Inner = ((x_OringInner-cx_Oring)**2)+((y_OringInner-cy_Oring)**2)
rad_Oring_Outer = np.sqrt(rad_Oring_Outer)
rad_Oring_Inner = np.sqrt(rad_Oring_Inner)
   
ang_Oring_Outer = np.arctan2((y_OringOuter-cy_Oring),(x_OringOuter-cx_Oring))* 180 / np.pi
ang_Oring_Inner = np.arctan2((y_OringInner-cy_Oring),(x_OringInner-cx_Oring))* 180/np.pi

def medfilt1(x,L):
	N = len(x)
	xin = np.array(x)
	filtered_Radius = np.zeros(xin.size)
	L = int(L)
	Lwing = (L-1)/2
	for i,xi in enumerate(xin):
		if i < Lwing:
			filtered_Radius[i] = np.median(xin[0:i+Lwing+1])
		elif i >= N - Lwing:
			filtered_Radius[i] = np.median(xin[i-Lwing:N])
		else:
			filtered_Radius[i] = np.median(xin[i-Lwing:i+Lwing+1])
	return filtered_Radius
if __name__ == '__main__':
	x=rad_Oring_Outer
	L = 51
	filtered_Radius = medfilt1(x,L)
	x1=rad_Oring_Inner
	filtered_Radius1 = medfilt1(x1,L)
	
	
filteredOutputInner= rad_Oring_Inner-filtered_Radius1
filteredOutputOuter= rad_Oring_Outer-filtered_Radius						
#~ plt.plot(ang_Oring_Inner,filteredOutputInner,'-')
plt.plot(ang_Oring_Outer,filteredOutputOuter,'-')
plt.grid(True)
plt.show()

absoluteValueOuter=np.abs(filteredOutputOuter)
absoluteValueOuter=absoluteValueOuter>2
absoluteValueOuter = absoluteValueOuter * 1

absoluteValueInner=np.abs(filteredOutputInner)
absoluteValueInner=absoluteValueInner>2
absoluteValueInner = absoluteValueInner * 1

#~ plt.plot(ang_Oring_Inner,rad_Oring_Inner,'.',color='g',markersize=2)
#~ plt.plot(ang_Oring_Outer,rad_Oring_Outer,'.',color='r',markersize=2)

if np.sum(absoluteValueInner) > 0:
	print 'reject'
elif np.sum(absoluteValueOuter) > 0:
	print 'reject'
else: 
	print 'ok' 

	
		
	

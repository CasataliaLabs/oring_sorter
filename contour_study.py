import cv2
import pylab
import time as time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.figure import Figure
from v4l2_capture_class import CaptureFromCam

'''if not 'cap' in locals():
	cap = cv2.VideoCapture()
if not cap.isOpened():
	cap.open(0)'''

#~ plt.ion()
#Capturing video frame
vidDevicePath = '/dev/video0'
if (not 'cap' in locals()): #| (cap.camLink == None):
	cap = CaptureFromCam(vidDevicePath)

if cap.camLink == None:
	cap = CaptureFromCam(vidDevicePath)
if cap.camLink == None:	
	print 'camera error'
	#~ exit()
	print 'test exit'
	sys.exit(0)	

frame = cap.read()
frameForDraw = frame 
frame_gray1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(frame_gray1,127,255, 128)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
k = 0
x_codnte = pylab.arange(0, 637, 1)
y_codnte = pylab.array([0] * 637)
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_title("Image capture")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.axis([-200,500 ,-100 ,500])
line1 = ax.plot(x_codnte, y_codnte, '-')
manager = plt.get_current_fig_manager()

while not k == -1:
	#~ for k in np.arange(0, len(contours)):
	cv2.drawContours(cap.read(), contours, k, (255,0,0),3)
	plt.imshow(frameForDraw)
	print 'contour number : ', k
	print contours
	#~ print "length of contours cell: ", len(contours[k])
	#~ print "the contour: ", contours[k]
	#~ print "hierachy is: ", hierarchy[0,k,:]
	k = raw_input('Enter to Continue: ')
	k = int(k)
	values = [0 for x in range(700)]
	#~ print "the contour",len(contours)
	#~ print len(values)
	for i in (len(contours)):
		if k==1:
			cnt_Oring = contours[k]
			x1 = cnt_Oring[:,:,0]
			x_Oring = x1[:,0]
			y1 = cnt_Oring[:,:,1]
			y_Oring = y1[:,0]
			Momnt_Oring = cv2.moments(cnt_Oring)
			print cnt_Oring
			cx_Oring = int(Momnt_Oring['m10']/Momnt_Oring['m00'])
			cy_Oring = int(Momnt_Oring['m01']/Momnt_Oring['m00'])
			rad_Oring = ((x_Oring-cx_Oring)**2)+((y_Oring-cy_Oring)**2)
			rad_Oring = np.sqrt(rad_Oring)
			#~ print rad_Oring
			ang_Oring = np.arctan2((y_Oring-cy_Oring),(x_Oring-cx_Oring))* 180/np.pi
			#print ang_Oring
			plt.plot(rad_Oring,ang_Oring)
			plt.show()
			
			def graphplot(arg):
				global frame_gray1, values,rad_Oring1,ang_Oring
				frame_gray2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
				values.append(rad_Oring)
				#~ print len(values)
				frame_gray2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
				frame_gray1 = frame_gray2
				CurrentXAxis = pylab.arange(len(values) -700 , len(values), 1)
				line1[0].set_data(CurrentXAxis, pylab.array(values[-700:]))
				ax.axis([CurrentXAxis.min(), CurrentXAxis.max()+1,-200,500])
				manager.canvas.draw()
				manager.show()
				pylab.show()
			if cv2.waitKey(1) & 0xFF == ord('q'):
				exit()

			timer = fig.canvas.new_timer(interval=20)
			timer.add_callback(graphplot, ())
			timer.start()
				
		#~ plt.plot(ang_Oring,rad_Oring)
		

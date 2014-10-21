__author__ = 'sreeram'
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.cm as cm
from Tkinter import *
from repeated_timer1 import RepeatedTimer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import time
from v4l2_capture_class import CaptureFromCam

plt.ion()


class ShowFrame():
	def __init__(self):
		self.kShowType = 0
		self.captureDevice = None
		self.axesFrame = None
		self.axesContour = None
		self.hIm = None
		self.imBw = None
		
		
	def showFrame(self):
		tic = time.time()
		self.frame = self.captureDevice.read()
				
		if self.frame == None:
			print 'camera read failed, line 140'
			return
		
		ret, imBw = cv2.threshold(self.frame,127,255,0)
		self.imBw = imBw
		self.axesFrame.clear()
		
		hIm = self.axesFrame.imshow(self.frame, cmap=cm.Greys_r)
		canvas1.show()
		toc = time.time()
		data = {'1': {'Time': '{0:.3f}'.format(toc - tic)}}
		model = table.model
		model.importDict(data)
		table.redrawTable()
		
	def oringRadius(self,oringContour):
		self.xOuter = oringContour
		self.xOuter1 = self.xOuter[:,:,0]
		self.x_OringOuter = self.xOuter1[:,0]
		self.yOuter=oringContour
		self.yOuter1 = self.yOuter[:,:,1]
		self.y_OringOuter = self.yOuter1[:,0]
			
		self.Momnt_Oring = cv2.moments(oringContour)
		self.cx_Oring = int(self.Momnt_Oring['m10']/self.Momnt_Oring['m00'])
		self.cy_Oring = int(self.Momnt_Oring['m01']/self.Momnt_Oring['m00'])
			
		self.rad_Oring_Outer = np.sqrt(((self.x_OringOuter-self.cx_Oring)**2)+((self.y_OringOuter-self.cy_Oring)**2))
		self.ang_Oring_Outer = np.arctan2((self.y_OringOuter-self.cy_Oring),(self.x_OringOuter-self.cx_Oring))* 180 / np.pi
		return self.rad_Oring_Outer,self.ang_Oring_Outer
	
	def medfilt1(self,radius):
		N = len(radius)
		xin = np.array(radius)
		self.filtered_Radiusnew = np.zeros(xin.size)
		L = 51
		Lwing = (L-1)/2
		for i,xi in enumerate(xin):
			if i < Lwing:
				self.filtered_Radiusnew[i] = np.median(xin[0:i+Lwing+1])
			elif i >= N - Lwing:
				self.filtered_Radiusnew[i] = np.median(xin[i-Lwing:N])
			else:
				self.filtered_Radiusnew[i] = np.median(xin[i-Lwing:i+Lwing+1])
		self.filteredOutput= abs(radius-self.filtered_Radiusnew)
		
		absoluteValueOuter=self.filteredOutput>2
		absoluteValueOuter = np.sum(absoluteValueOuter * 1)

		return self.filteredOutput,absoluteValueOuter
		
	def showContour(self):
		self.AreaOfBackGroundContour = []
		
		contours, hierarchy = cv2.findContours(self.imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
		bgImageForContourPlot = np.zeros(self.imBw.shape)
		self.parent = hierarchy[0,:,3]
		self.backGround = self.parent == -1
		self.indexOfBackGround= np.where(self.backGround == True)[0]
		for iteration in range(0,len(self.indexOfBackGround)):
			self.AreaOfBackGroundContour.append(cv2.contourArea(contours[self.indexOfBackGround[iteration]]))
		self.maxAreaOfBackGround = np.max(self.AreaOfBackGroundContour)
		self.indexOfBigBackGround = self.AreaOfBackGroundContour.index(self.maxAreaOfBackGround)
		
		self.childOuter = self.parent == self.indexOfBackGround[self.indexOfBigBackGround]
		self.IndexOfZeroParentOuter= np.where(self.childOuter == True)[0]
		
		for iterationOuter in range(0,len(self.IndexOfZeroParentOuter)):
			self.AreaOfContourOuter=cv2.contourArea(contours[self.IndexOfZeroParentOuter[iterationOuter]])
			if self.AreaOfContourOuter >10000:
				if list(self.parent).count(self.IndexOfZeroParentOuter[iterationOuter])==1:
					radius,angle = self.oringRadius(contours[self.IndexOfZeroParentOuter[iterationOuter]])
					filteredOutput, absoluteValueOuter = self.medfilt1(radius)
					if absoluteValueOuter>0:
						cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter],(255,0,0),-1)
					else:
						cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter], 255, 2)
						
						innerContourIndex = list(self.parent).index(self.IndexOfZeroParentOuter[iterationOuter])
						innerContour = contours[innerContourIndex]
						
						radiusInner,angleInner = self.oringRadius(innerContour)
						filteredOutput, absoluteValueOuter = self.medfilt1(radiusInner)
						if absoluteValueOuter>0:
							cv2.drawContours(bgImageForContourPlot, contours,innerContourIndex,(255,0,0),-1)
						else:
							cv2.drawContours(bgImageForContourPlot, contours,innerContourIndex,255,2) 
				else:
					cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter],(255,0,0),-1)		
			else:
				cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter],(255,0,0),-1)	
					
		hIm = self.axesContour.imshow(bgImageForContourPlot, cmap=cm.Greys_r)
		canvas2.show()
						
def video_start():
    timerFrameDisplay.start()
    timerFrameContour.start()
   
def video_stop():
    timerFrameDisplay.stop()
    timerFrameContour.stop()

vidDevicePath = '/dev/video1*'
if (not 'cap' in locals()): #| (cap.camLink == None):
	cap = CaptureFromCam(vidDevicePath)

if cap.camLink == None:
	cap = CaptureFromCam(vidDevicePath)
if cap.camLink == None:	
	print 'camera error'
	print 'test exit'
	sys.exit(0)

frame = cap.read()

master = Tk()
master.title("Oring GUI")
screenWidth=master.winfo_screenwidth()
screenHeight=master.winfo_screenheight()
master.geometry(("%dx%d")%(screenWidth,screenHeight)) 

figure1 = Figure(figsize=(4, 4), dpi=100)
axesFrame = figure1.add_subplot(111)
figure1 .suptitle("ORINGS")
hIm = axesFrame.imshow(frame,cmap = cm.Greys_r, vmin=20, vmax=80)

canvas1 = FigureCanvasTkAgg(figure1 , master=master)
canvas1.get_tk_widget().place(x=10, y=20)

x_codnte = np.arange(0, 100, 1)
y_codnte = np.array([0] * 100)

figure2 = Figure(figsize=(5, 4.5), dpi=90)
axesContour = figure2.add_subplot(111)
figure2 .suptitle("CONTOUR PLOTS")

canvas2 = FigureCanvasTkAgg(figure2, master=master)
canvas2.get_tk_widget().place(x=450, y=20)

frame_value = Frame(master)
frame_value.pack()
frame_value.place(x=100, y=500,width=300, height=70)
model = TableModel()
table = TableCanvas(frame_value, model=model, editable=False)
table.createTableFrame()


objShowFrame = ShowFrame()
objShowFrame.captureDevice = cap
objShowFrame.axesFrame = axesFrame
objShowFrame.axesContour = axesContour
objShowFrame.hIm = hIm

timerFrameDisplay = figure1.canvas.new_timer(interval=1)
timerFrameDisplay.add_callback(objShowFrame.showFrame)

timerFrameContour = figure2.canvas.new_timer(interval=1)
timerFrameContour.add_callback(objShowFrame.showContour)

b1 = Button(master, text="Start", bg='white', command=video_start).place(x=50, y=600)
b2 = Button(master, text="Stop", bg='white', command=video_stop).place(x=400, y=600)
#~ master.mainloop()

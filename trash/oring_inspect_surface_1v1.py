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

vidDevicePath = '/dev/video1'
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
master.geometry("1000x1000") #how to set full screen

figure1 = Figure(figsize=(4, 4), dpi=100)
axesFrame = figure1.add_subplot(111)
figure1 .suptitle("Live Video")
hIm = axesFrame.imshow(frame,cmap = cm.Greys_r, vmin=20, vmax=80)

canvas1 = FigureCanvasTkAgg(figure1 , master=master)
canvas1.get_tk_widget().place(x=10, y=20)


x_codnte = np.arange(0, 100, 1)
y_codnte = np.array([0] * 100)

figure2 = Figure(figsize=(5, 4.5), dpi=90)
axesContour = figure2.add_subplot(111)

canvas2 = FigureCanvasTkAgg(figure2, master=master)
canvas2.get_tk_widget().place(x=450, y=20)

frame_value = Frame(master)
frame_value.pack()
frame_value.place(x=100, y=500,width=300, height=70)
model = TableModel()
table = TableCanvas(frame_value, model=model, editable=False)
table.createTableFrame()


class ShowFrame():
	def __init__(self):
		self.kShowType = 0
		self.captureDevice = None
		self.axes = None
		self.hIm = None
		self.axesFrame = None
		self.imBw = None
		self.axesContour = None
		
		
		
	def showContour(self):
		imBw = self.imBw
		self.AreaOfContourOuter = []
		self.outRadIndexForLogic=[]
		self.inRadIndexForLogic=[]
		self.cnt_OringOuter=[]
		self.cnt_OringInner=[]	
		self.radiusOuter=[]
		self.radiusInner=[]
		self.angOuter=[]
		self.angInner=[]
		contours, hierarchy = cv2.findContours(imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		#~ print "contours length", len(contours)
		
		bgImageForContourPlot = np.zeros(imBw.shape)
		self.parent = hierarchy[0,:,3]
		
		self.backGround = self.parent == -1
		self.indexOfBackGround= np.where(self.backGround == True)[0]
		self.AreaOfBackGroundContour = []
		for iteration in range(0,len(self.indexOfBackGround)):
			self.AreaOfBackGroundContour.append(cv2.contourArea(contours[self.indexOfBackGround[iteration]]))
		self.maxAreaOfBackGround = np.max(self.AreaOfBackGroundContour)
		self.indexOfBigBackGround = self.AreaOfBackGroundContour.index(self.maxAreaOfBackGround)
		self.childOuter = self.parent == self.indexOfBackGround[self.indexOfBigBackGround]
		self.IndexOfZeroParentOuter= np.where(self.childOuter == True)[0]
							
		for iterationOuter in range(0,len(self.IndexOfZeroParentOuter)):
			self.AreaOfContourOuter.append(cv2.contourArea(contours[self.IndexOfZeroParentOuter[iterationOuter]]))
			if self.AreaOfContourOuter[iterationOuter] >5000:
				self.cnt_OringOuter.append(contours[self.IndexOfZeroParentOuter[iterationOuter]])
				self.outRadIndexForLogic.append(self.IndexOfZeroParentOuter[iterationOuter])
				cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter], 255, 3)
				self.childInner = self.parent == self.IndexOfZeroParentOuter[iterationOuter]
				self.IndexOfZeroParentInner= np.where(self.childInner == True)[0]
				self.AreaOfContourInner = []
				for iterationInner in range(0,len(self.IndexOfZeroParentInner)):
					self.AreaOfContourInner.append(cv2.contourArea(contours[self.IndexOfZeroParentInner[iterationInner]]))
					if self.AreaOfContourInner[iterationInner] > 1000:
						self.cnt_OringInner.append(contours[self.IndexOfZeroParentInner[iterationInner]])
						self.inRadIndexForLogic.append(self.IndexOfZeroParentInner[iterationInner])
						cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentInner[iterationInner],255,3) 
				
		hIm = self.axesContour.imshow(bgImageForContourPlot, cmap=cm.Greys_r)
		canvas2.show()
		for iterationrad in range(0,len(self.outRadIndexForLogic)):
			self.radiusOuter.append(self.oringLogic(iterationrad))
			self.radiusInner.append(self.oringLogic(iterationrad)) 	
			self.angOuter.append(self.oringLogic(iterationrad))
			self.angInner.append(self.oringLogic(iterationrad))
		print "Inner angle",self.angInner		
			
	def oringLogic(self,i):
		self.xOuter = self.cnt_OringOuter[i]
		self.xOuter1 = self.xOuter[:,:,0]
		self.x_OringOuter = self.xOuter1[:,0]
		self.yOuter=self.cnt_OringOuter[i]
		self.yOuter1 = self.yOuter[:,:,1]
		self.y_OringOuter = self.yOuter1[:,0]
		
		self.xInner = self.cnt_OringInner[i]
		self.xInner1 = self.xInner[:,:,0]
		self.x_OringInner = self.xInner1[:,0]
		self.yInner = self.cnt_OringInner[i]
		self.yInner1 = self.yInner[:,:,1]
		self.y_OringInner = self.yInner1[:,0]
			
		self.Momnt_Oring = cv2.moments(self.cnt_OringOuter[i])
		self.cx_Oring = int(self.Momnt_Oring['m10']/self.Momnt_Oring['m00'])
		self.cy_Oring = int(self.Momnt_Oring['m01']/self.Momnt_Oring['m00'])
			
		self.rad_Oring_Outer = np.sqrt(((self.x_OringOuter-self.cx_Oring)**2)+((self.y_OringOuter-self.cy_Oring)**2))
		self.rad_Oring_Inner = np.sqrt(((self.x_OringInner-self.cx_Oring)**2)+((self.y_OringInner-self.cy_Oring)**2))
		self.ang_Oring_Outer = np.arctan2((self.y_OringOuter-self.cy_Oring),(self.x_OringOuter-self.cx_Oring))* 180 / np.pi
		self.ang_Oring_Inner = np.arctan2((self.y_OringInner-self.cy_Oring),(self.x_OringInner-self.cx_Oring))* 180/np.pi
		return self.rad_Oring_Outer,self.rad_Oring_Inner,self.ang_Oring_Outer,self.ang_Oring_Inner
	
	    
		
		
		#~ def medfilt1(x,L):
			#~ N = len(x)
			#~ xin = np.array(x)
			#~ filtered_Radius = np.zeros(xin.size)
			#~ L = int(L)
			#~ Lwing = (L-1)/2
			#~ for i,xi in enumerate(xin):
				#~ if i < Lwing:
					#~ filtered_Radius[i] = np.median(xin[0:i+Lwing+1])
				#~ elif i >= N - Lwing:
					#~ filtered_Radius[i] = np.median(xin[i-Lwing:N])
				#~ else:
					#~ filtered_Radius[i] = np.median(xin[i-Lwing:i+Lwing+1])
			#~ return filtered_Radius
		#~ if __name__ == '__main__':
			#~ x=self.rad_Oring_Outer
			#~ L = 51
			#~ filtered_Radius = medfilt1(x,L)
			#~ x1=self.rad_Oring_Inner
			#~ filtered_Radius1 = medfilt1(x1,L)
		#~ 
		#~ filteredOutputInner= filtered_Radius1-self.rad_Oring_Inner
		#~ filteredOutputOuter= self.rad_Oring_Outer-filtered_Radius
		
			
	def showFrame(self):
		tic = time.time()
		self.frame = self.captureDevice.read()
		#~ cv2.imwrite("oringblue.jpg",self.frame)
		
		if self.frame == None:
			print 'camera read failed, line 140'
			return
		
		
		ret, imBw = cv2.threshold(self.frame,127,255,0)
		self.imBw = imBw
		self.axes.clear()
		
		hIm = self.axes.imshow(self.frame, cmap=cm.Greys_r)
		#~ self.hIm = hIm
		canvas1.show()
		toc = time.time()
		data = {'1': {'Time': '{0:.3f}'.format(toc - tic)}}
		model = table.model
		model.importDict(data)
		table.redrawTable()
		#~ return hIm
		
	

def video_start():
    timerFrameDisplay.start()
    timerFrameContour.start()
   
def video_stop():
    timerFrameDisplay.stop()
    timerFrameContour.stop()


objShowFrame = ShowFrame()
objShowFrame.captureDevice = cap
objShowFrame.axes = axesFrame
objShowFrame.axesContour = axesContour
objShowFrame.hIm = hIm

timerFrameDisplay = figure1.canvas.new_timer(interval=1)
timerFrameDisplay.add_callback(objShowFrame.showFrame)

timerFrameContour = figure2.canvas.new_timer(interval=1)
timerFrameContour.add_callback(objShowFrame.showContour)

b1 = Button(master, text="Start", bg='white', command=video_start).place(x=50, y=600)
b2 = Button(master, text="Stop", bg='white', command=video_stop).place(x=400, y=600)
#~ master.mainloop()
#~ canvas1.mpl_connect('button_press_event', objShowFrame.changeFrame)

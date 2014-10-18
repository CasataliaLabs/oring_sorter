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

vidDevicePath = '/dev/video0*'
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
		contours, hierarchy = cv2.findContours(imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		print "The hierarchy is",hierarchy
		#~ print "contours length", len(contours)
		
		bgImageForContourPlot = np.zeros(imBw.shape)
		self.parent = hierarchy[0,:,3]
		
		
		self.backGround = self.parent == -1
		print "selfbackground",self.backGround
		self.indexOfBackGround= np.where(self.backGround == True)[0]
		self.AreaOfBackGroundContour = []
		for iteration in range(0,len(self.indexOfBackGround)):
			self.AreaOfBackGroundContour.append(cv2.contourArea(contours[self.indexOfBackGround[iteration]]))
		self.maxAreaOfBackGround = np.max(self.AreaOfBackGroundContour)
		self.indexOfBigBackGround = self.AreaOfBackGroundContour.index(self.maxAreaOfBackGround)
		print "index of bigbackground",self.indexOfBigBackGround 
		self.childOuter = self.parent == self.indexOfBackGround[self.indexOfBigBackGround]
		self.IndexOfZeroParentOuter= np.where(self.childOuter == True)[0]
		self.AreaOfContourOuter = []
		
		for iteration in range(0,len(self.IndexOfZeroParentOuter)):
			self.AreaOfContourOuter.append(cv2.contourArea(contours[self.IndexOfZeroParentOuter[iteration]]))
		for iterationOuter in range(0,len(self.IndexOfZeroParentOuter)):
			if self.AreaOfContourOuter[iterationOuter] >7000:
				cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter], 255, 3)
				self.childInner = self.parent == self.IndexOfZeroParentOuter[iterationOuter]
				self.IndexOfZeroParentInner= np.where(self.childInner == True)[0]
				self.AreaOfContourInner = []
				for iteration in range(0,len(self.IndexOfZeroParentInner)):
					self.AreaOfContourInner.append(cv2.contourArea(contours[self.IndexOfZeroParentInner[iteration]]))
				for iterationInner in range(0,len(self.IndexOfZeroParentInner)):
					if self.AreaOfContourInner > 1700:
						cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentInner[iterationInner],255,3) 
			
											
		hIm = self.axesContour.imshow(bgImageForContourPlot, cmap=cm.Greys_r)
		canvas2.show()
		
			
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

#~ master.mainloop()
#~ canvas1.mpl_connect('button_press_event', objShowFrame.changeFrame)

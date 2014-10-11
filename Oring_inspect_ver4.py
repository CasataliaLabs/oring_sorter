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

vidDevicePath = '/dev/video0'
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
axisFrame = figure1.add_subplot(111)
figure1 .suptitle("Live Video")
hIm = axisFrame.imshow(frame,cmap = cm.Greys_r, vmin=20, vmax=80)

canvas1 = FigureCanvasTkAgg(figure1 , master=master)
canvas1.get_tk_widget().place(x=10, y=20)


x_codnte = np.arange(0, 100, 1)
y_codnte = np.array([0] * 100)

figure2 = Figure(figsize=(5, 4.5), dpi=90)
axisGraph = figure2.add_subplot(111)

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
		
	def showGraph(self):
		self.xOuter = self.cnt_OringOuter[:,:,0]
		self.xInner = self.cnt_OringInner[:,:,0]
		self.x_OringOuter = self.xOuter[:,0]
		self.x_OringInner = self.xInner[:,0]
		self.yOuter = self.cnt_OringOuter[:,:,1]
		self.yInner = self.cnt_OringInner[:,:,1]
		self.y_OringOuter = self.yOuter[:,0]
		self.y_OringInner = self.yInner[:,0]
		self.Momnt_Oring = cv2.moments(self.cnt_OringOuter)
		self.cx_Oring = int(self.Momnt_Oring['m10']/self.Momnt_Oring['m00'])
		self.cy_Oring = int(self.Momnt_Oring['m01']/self.Momnt_Oring['m00'])
		self.rad_Oring_Outer = np.sqrt(((self.x_OringOuter-self.cx_Oring)**2)+((self.y_OringOuter-self.cy_Oring)**2))
		self.rad_Oring_Inner = np.sqrt(((self.x_OringInner-self.cx_Oring)**2)+((self.y_OringInner-self.cy_Oring)**2))
		
		self.ang_Oring_Outer = np.arctan2((self.y_OringOuter-self.cy_Oring),(self.x_OringOuter-self.cx_Oring))* 180 / np.pi
		self.ang_Oring_Inner = np.arctan2((self.y_OringInner-self.cy_Oring),(self.x_OringInner-self.cx_Oring))* 180/np.pi
		
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
			x=self.rad_Oring_Outer
			L = 51
			filtered_Radius = medfilt1(x,L)
			x1=self.rad_Oring_Inner
			filtered_Radius1 = medfilt1(x1,L)
		
		filteredOutputInner= filtered_Radius1-self.rad_Oring_Inner
		filteredOutputOuter= self.rad_Oring_Outer-filtered_Radius
		
		
		absoluteValueOuter=np.abs(filteredOutputOuter)
		absoluteValueOuter=absoluteValueOuter>1
		absoluteValueOuter = absoluteValueOuter * 1

		absoluteValueInner=np.abs(filteredOutputInner)
		absoluteValueInner=absoluteValueInner>1
		absoluteValueInner = absoluteValueInner * 1
				
		if np.sum(absoluteValueInner) > 0:
			print 'reject'
			#~ label = Label(master,text = 'Reject')
		elif np.sum(absoluteValueOuter) > 0:
			#~ label = Label(master,text = 'Reject')
			print 'reject'
		else: 
			#~ label = Label(master,text = 'Ok')
			print 'ok'
		
		axisGraph.clear()
		axisGraph.grid()
		axisGraph.set_title("Graph Plot")
		axisGraph.set_xlabel("Angle")
		axisGraph.set_ylabel("Radius")
		axisGraph.plot(self.ang_Oring_Outer,filteredOutputOuter, color='r', marker='s', markersize=2)
		canvas2.show()
		
			
	def showFrame(self):
		tic = time.time()
		self.frame = self.captureDevice.read()
		
		if self.frame == None:
			print 'camera read failed, line 140'
			return
		
		gray_scale = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
		ret, imBw = cv2.threshold(gray_scale,127,255,0)
		
		self.axes.clear()
		if self.kShowType == 0:
			hIm = self.axes.imshow(self.frame[:,:,[2,1,0]])
		
		elif self.kShowType == 1:
			
			hIm = self.axes.imshow(gray_scale, cmap=cm.Greys_r)
		elif self.kShowType == 2:
			hIm = self.axes.imshow(imBw, cmap=cm.Greys_r)
			
			
		else:
			contours, hierarchy = cv2.findContours(imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
						
			try:
				if hierarchy != None:
					bgImageForContourPlot = np.zeros(imBw.shape)
									
					self.parentOuter = hierarchy[0,:,3]
					self.childOuter = self.parentOuter == 0
					self.IndexOfZeroParentOuter= np.where(self.childOuter == True)[0]
						
					self.AreaOfContourOuter = []
					for iteration in range(0,len(self.IndexOfZeroParentOuter)):
						self.AreaOfContourOuter.append(cv2.contourArea(contours[self.IndexOfZeroParentOuter[iteration]]))
					
					self.AreaOfContourMaxOuter = np.max(self.AreaOfContourOuter)
					self.IndexOfMaximumAreaOuter = self.AreaOfContourOuter.index(self.AreaOfContourMaxOuter)
					
					self.parentInner = hierarchy[0,:,3]
					self.childInner = self.parentInner == self.IndexOfZeroParentOuter[self.IndexOfMaximumAreaOuter]
					self.IndexOfZeroParentInner= np.where(self.childInner == True)[0]
					self.AreaOfContourInner = []
						
					for iteration in range(0,len(self.IndexOfZeroParentInner)):
						self.AreaOfContourInner.append(cv2.contourArea(contours[self.IndexOfZeroParentInner[iteration]]))
					
					self.AreaOfContourMaxInner = np.max(self.AreaOfContourInner)
					self.IndexOfMaximumAreaInner = self.AreaOfContourInner.index(self.AreaOfContourMaxInner)
					
		
					for noParentsIndex in range(0,len(self.IndexOfZeroParentOuter)):
						if noParentsIndex == self.IndexOfMaximumAreaOuter:
							self.cnt_OringOuter = contours[self.IndexOfZeroParentOuter[self.IndexOfMaximumAreaOuter]]
							cv2.drawContours(bgImageForContourPlot, contours, self.IndexOfZeroParentOuter[self.IndexOfMaximumAreaOuter], 255, 2)
							hIm = self.axes.imshow(bgImageForContourPlot, cmap=cm.Greys_r)
													
					for noParentsIndex in range(0,len(self.IndexOfZeroParentInner)):
						if noParentsIndex == self.IndexOfMaximumAreaInner:
							self.cnt_OringInner = contours[self.IndexOfZeroParentInner[self.IndexOfMaximumAreaInner]]
							cv2.drawContours(bgImageForContourPlot, contours, self.IndexOfZeroParentInner[self.IndexOfMaximumAreaInner], 255, 2)
							hIm = self.axes.imshow(bgImageForContourPlot, cmap=cm.Greys_r)
											
						self.showGraph()
					
						
						
			except:
				print "Oring Out of Focus"
				contours, hierarchy = cv2.findContours(imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				bgImageForContourPlot = np.zeros(imBw.shape)
				cv2.drawContours(bgImageForContourPlot, contours, -1, 255, 2)
				hIm = self.axes.imshow(bgImageForContourPlot, cmap=cm.Greys_r)
									
		
		canvas1.show()
		toc = time.time()
		data = {'1': {'Time': '{0:.3f}'.format(toc - tic),'Gray_value': '{}'.format(gray_scale.min())}}
		model = table.model
		model.importDict(data)
		table.redrawTable()
		#~ return hIm
		
	def changeFrame(self, event):
		if self.kShowType <= 2:
			self.kShowType = self.kShowType + 1
		else:
			self.kShowType = 0
			
		print "ShowFrameType k upgraded to: ", self.kShowType

def video_start():
    timerFrameDisplay.start()
   
def video_stop():
    timerFrameDisplay.stop()

objShowFrame = ShowFrame()
objShowFrame.captureDevice = cap
objShowFrame.axes = axisFrame
objShowFrame.axesFrame = axisGraph
objShowFrame.hIm = hIm

timerFrameDisplay = figure2.canvas.new_timer(interval=-1)
timerFrameDisplay.add_callback(objShowFrame.showFrame)


b1 = Button(master, text="Start", bg='white', command=video_start).place(x=50, y=600)
b2 = Button(master, text="Stop", bg='white', command=video_stop).place(x=400, y=600)
#~ master.mainloop()
canvas1.mpl_connect('button_press_event', objShowFrame.changeFrame)


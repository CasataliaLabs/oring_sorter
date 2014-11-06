__author__ = 'sreeram'
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.cm as cm
import Tkinter
from Tkinter import Tk
from Tkinter import *
import tkMessageBox as MessageBox 
from repeated_timer1 import RepeatedTimer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import time
from v4l2_capture_class import CaptureFromCam
from PIL import ImageTk, Image
import os

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
		#~ if objShowFrame.hIm == None:
			#~ self.axesFrame.clear()
			#~ self.hIm = self.axesFrame.imshow(self.frame, cmap=cm.Greys_r)
			#~ print 'if executing'
		#~ else:
		self.hIm.set_data(self.frame)
			#~ print 'else exectuing'
		tic = time.time()
		#~ canvasShowFrame.draw()
		figureShowFrame.canvas.draw()
		toc = time.time()
		data = {'1': {'Time': '{0:.3f}'.format(toc - tic)}}
		model = table.model
		model.importDict(data)
		table.redrawTable()
		#~ toc = time.time()
		print toc - tic
	def oringRadius(self,oringContour):
		self.xOring = oringContour
		self.xOring1 = self.xOring[:,:,0]
		self.x_Oring = self.xOring1[:,0]
		self.yOring=oringContour
		self.yOring1 = self.yOring[:,:,1]
		self.y_Oring = self.yOring1[:,0]
			
		self.Momnt_Oring = cv2.moments(oringContour)
		self.cx_Oring = int(self.Momnt_Oring['m10']/self.Momnt_Oring['m00'])
		self.cy_Oring = int(self.Momnt_Oring['m01']/self.Momnt_Oring['m00'])
			
		self.rad_Oring = np.sqrt(((self.x_Oring-self.cx_Oring)**2)+((self.y_Oring-self.cy_Oring)**2))
		self.ang_Oring = np.arctan2((self.y_Oring-self.cy_Oring),(self.x_Oring-self.cx_Oring))* 180 / np.pi
		return self.rad_Oring,self.ang_Oring
	
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
		canvasShowContour.show()
						
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
img = Tkinter.Image("photo", file="drishtiman.gif")
master.tk.call('wm','iconphoto',master._w,img) 

top = Toplevel(master = master)
top.attributes("-topmost", 1)


#~ Menu construction-- file menu
def hello():
    masterlabel=Label(master, text="hello").pack()
    return
def about():
	MessageBox.showinfo(title="About",message="Automatic Oring Inspection Project")
	return
menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New",command=hello)
filemenu.add_command(label="save")
filemenu.add_command(label="quit", command=master.quit)
menubar.add_cascade(label="file",menu=filemenu)
#~ master.config(menu=menubar)

#~ help menu
helpmenu = Menu(menubar, tearoff=False)
helpmenu.add_command(label="Help Docs",command=hello)
helpmenu.add_command(label="About",command=about)
menubar.add_cascade(label="Help",menu=helpmenu)
master.config(menu=menubar)

#~ start and stopmenu
startmenu = Menu(menubar, tearoff=False)
startmenu.add_command(label="Start",command=video_start)
startmenu.add_command(label="Stop",underline=0,command=video_stop,accelerator="Ctrl+Q")
menubar.add_cascade(label="Run",underline=0,menu=startmenu)
master.config(menu=menubar)
master.bind('<Shift-Q>', video_stop)

#~ startmenu = Menu(menubar, tearoff=False)
#~ startmenu.add_command(label="Start",command=video_start)
#~ startmenu.add_command(label="Stop",command=video_stop)
#~ menubar.add_cascade(label="Run",menu=startmenu)
#~ master.config(menu=menubar)


#~ Drishtiman Image
img = ImageTk.PhotoImage(Image.open("drishtiman.jpg"))
panel = Label(master, image = img)
panel.place(x=1200,y=550)



figureShowFrame = Figure(figsize=(4, 4), dpi=100)
axesFrame = figureShowFrame.add_subplot(111)
figureShowFrame.suptitle("ORINGS")
#~ hIm = axesFrame
hIm = axesFrame.imshow(frame, interpolation='nearest', cmap = cm.Greys_r, vmin=20, vmax=80, animated=True)

canvasShowFrame = FigureCanvasTkAgg(figureShowFrame , master=master)
canvasShowFrame.get_tk_widget().place(x=150, y=100)

#~ x_codnte = np.arange(0, 100, 1)
#~ y_codnte = np.array([0] * 100)

figureShowContour = Figure(figsize=(4, 4), dpi=100)
axesContour = figureShowContour.add_subplot(111)
figureShowContour.suptitle("CONTOUR PLOTS")


def deletewidget():
	canvasShowContour.get_tk_widget().delete("all")
	
canvasShowContour = FigureCanvasTkAgg(figureShowContour, master=master)
canvasShowContour.get_tk_widget().place(x=750, y=100)




frame_value = Frame(master)
frame_value.pack()
frame_value.place(x=500, y=550,width=300, height=70)
model = TableModel()
table = TableCanvas(frame_value, model=model, editable=False)
table.createTableFrame()


objShowFrame = ShowFrame()
objShowFrame.captureDevice = cap
objShowFrame.axesFrame = axesFrame
objShowFrame.axesContour = axesContour
objShowFrame.hIm = hIm

timerFrameDisplay = figureShowFrame.canvas.new_timer(interval=100)
timerFrameDisplay.add_callback(objShowFrame.showFrame)

timerFrameContour = figureShowContour.canvas.new_timer(interval=1)
timerFrameContour.add_callback(objShowFrame.showContour)

b1 = Button(master, text="DeleteWidget", bg='white', command=deletewidget,height=2,width=10).place(x=1200,y=300)
#~ b2 = Button(master, text="Widget", bg='white', command=widget).place(x=800, y=630)
#~ master.mainloop()

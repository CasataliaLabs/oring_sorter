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
import matplotlib.cm as cm
#~ import os

plt.ion()
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
#~ if not cap.isOpened():
	#~ cap.open(0)
#~ gray_1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
frame = cap.read()
#~ frameForDraw = frame * 1
#~ cv2.imwrite("Image.jpg",frame)
#~ if ret == 0:
	#~ cap.release()
	#~ cap.open(1)
	#~ ret, frame = cap.read()
	#~ print 'cam failed, second attempt'

#Creating window with title and= geometry
master = Tk()
master.title("Oring GUI")
master.geometry("1000x1000") #how to set full screen


#Creating figure for showing video frame
f1 = Figure(figsize=(4, 4), dpi=100)
axis1 = f1.add_subplot(111)
f1.suptitle("Live Video")
hIm = axis1.imshow(frame,cmap = cm.Greys_r, vmin=20, vmax=80)

print 'test'
#Creating canvass for placing video frame
canvas1 = FigureCanvasTkAgg(f1, master=master)
canvas1.get_tk_widget().place(x=10, y=20)
#~ sys.exit()

# defining axis from the figures
x_codnte = np.arange(0, 100, 1)
y_codnte = np.array([0] * 100)

#Creating figure for plotting the frame variations
f2 = Figure(figsize=(4, 4.4), dpi=100)
ax = f2.add_subplot(111)

#Creating canvas for plotting the frame variations
canvas2 = FigureCanvasTkAgg(f2, master=master)
canvas2.get_tk_widget().place(x=500, y=30)

#Setting the title and labels for the plot
ax.grid(True)
ax.set_title("Graph Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.axis([0, 100, 0, 255])

#Plotting the x,y axis , setting value zero array to access values
line1 = ax.plot(x_codnte, y_codnte, '-', color='r', marker='s', markersize=2)
manager = plt.get_current_fig_manager()
values = [0 for x in range(100)]

# table creation
frame_value = Frame(master)
frame_value.pack()
frame_value.place(x=100, y=500,width=300, height=70)
model = TableModel()
table = TableCanvas(frame_value, model=model, editable=False)
table.createTableFrame()

#Function for the acquiring values for plotting the frame variations
def showGraph(arg):
	tic = time.time()
	global frame, values
	CurrentXAxis = pylab.arange(len(values) - 100, len(values), 1)
	line1[0].set_data(CurrentXAxis, pylab.array(values[-100:]))
	ax.axis([CurrentXAxis.min(), CurrentXAxis.max() + 1, 0, 255])
	manager.canvas.draw()
	pylab.draw()
	canvas2.show()
	toc = time.time()
	print "showGraphTime", (toc -  tic)

	#~ print '\nClicked at: x=',event.x,'  y=',event.y
	#~ ret,frame = cap.read()
	#~ if ret == None:
		#~ print "cap.read() failed"
		#~ return
	#~ hIm.set_array(frame)
	#~ canvas1.show()
	#~ canvas1.mpl_connect('button_press_event1', click1)
	
#~ def click1(event1):
	#~ print '\nClicked at: x=',event1.x,'  y=',event1.y
	#~ ret,frame = cap.read()
	#~ if ret == None:
		#~ print "cap.read() failed"
		#~ return
	#~ gray_scale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#~ hIm.set_array(gray_scale)
	#~ canvas1.show()
	#~ canvas1.mpl_connect('button_press_event', click)
	
				
#Function to display video frame,mean of frame variations,display in a table
class ShowFrame():
	def __init__(self):
		self.kShowType = 0
		self.captureDevice = None
		self.axes = None
		self.hIm = None
		
		
	def showFrame(self):
		tic = time.time()
		self.frame = self.captureDevice.read()
		if self.frame == None:
			print 'camera read failed, line 140'
			return
		#~ if ret == 0:
			#~ print "reading from camera failed"
		gray_scale = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
		ret, imBw = cv2.threshold(gray_scale,127,255,0)
		#~ contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		#~ imBw = gray_scale	> 128
		#~ imBw = imBw * 255
		#~ imBw = np.astype('uint8')
		#~ imBw
		self.axes.clear()
		if self.kShowType == 0:
			hIm = self.axes.imshow(self.frame[:,:,[2,1,0]])
			#~ self.hIm.set_array(self.frame[:,:,[2,1,0]])
		#~ hIm.set_array(self.frame[:,:,[2,1,0]])
		elif self.kShowType == 1:
			
			hIm = self.axes.imshow(gray_scale, cmap=cm.Greys_r)
		elif self.kShowType == 2:
			hIm = self.axes.imshow(imBw, cmap=cm.Greys_r)
			
		else:
			#~ gray_scale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			#~ ret,thresh = cv2.threshold(frame_gray1,0,255, 128) #cv2.THRESH_OTSU)
			contours, hierarchy = cv2.findContours(imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			bgImageForContourPlot = np.zeros(imBw.shape)
			cv2.drawContours(bgImageForContourPlot, contours, 1, (255,0,0), 2)
			hIm = self.axes.imshow(bgImageForContourPlot, cmap=cm.Greys_r)
		
		#~ plt.show()
		canvas1.show()
		toc = time.time()
		#~ print toc - tic
		data = {'1': {'Time': '{0:.3f}'.format(toc - tic),'Gray_value': '{}'.format(gray_scale.min())}}
		model = table.model
		model.importDict(data)
		table.redrawTable()
		return hIm
	def changeFrame(self, event):
		if self.kShowType <= 2:
			self.kShowType = self.kShowType + 1
		else:
			self.kShowType = 0
			#~ print self.kShowType, "kShowType"
		print "ShowFrameType k upgraded to: ", self.kShowType
#Function for starting timers
def video_start():
    timerFrameDisplay.start()
    #~ t.start()
    
#Function for stopping timers
def video_stop():
    timerFrameDisplay.stop()
    #~ t.stop()

objShowFrame = ShowFrame()
objShowFrame.captureDevice = cap
objShowFrame.axes = axis1
objShowFrame.hIm = hIm

#Timer for frame
timerFrameDisplay = f2.canvas.new_timer(interval=0)
timerFrameDisplay.add_callback(objShowFrame.showFrame)

#Timer for video
#~ t = RepeatedTimer(0.01, video)

#Start and Stop Buttons
b1 = Button(master, text="Start", bg='white', command=video_start).place(x=50, y=600)
b2 = Button(master, text="Stop", bg='white', command=video_stop).place(x=400, y=600)
#~ master.mainloop()



#~ kShowFrameType = KShowFrameType(0)
#~ KShowFrameType(0)

#~ canvas1.mpl_connect('button_press_event', lambda e: ShowFrame().callback(e,kShowFrameType))
canvas1.mpl_connect('button_press_event', objShowFrame.changeFrame)
#~ kShowFrameType = 0


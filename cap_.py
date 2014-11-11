import Tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
from glob import glob
from v4l2_capture_class import CaptureFromCam
#~ import matplotlib.pyplot as plt
import numpy as np

class Cap():
	def __init__(self):
		#~ self.root = tk.Toplevel()
		#~ self.root = tk.Tk()
		#~ self.root.attributes('-zoomed', True)
		#~ self.root.attributes('-fullscreen', True)
		#~ self.isWinPresent = True
		#~ self.root.protocol('WM_DELETE_WINDOW', self.removewindow)

		#~ self._menubar = tk.Menu(self.root)
		#~ self._menubar.add_command(label="Start", command=self.startTimer)
		#~ self._menubar.add_command(label="Stop", command=self.stopTimer)
		#~ self.root.config(menu=self._menubar) # display the menu
		self.timerInterval = 8
		self.timerCommand = False
		self.cam = None
		#~ self.label1 = None
		
		#~ self.root.wm_iconbitmap('@drishtiman_icon.xbm')
		#~ self.root.title('Drishtiman')
	
	def camReadV4l(self):
		if self.cam == None:
			self.cam = CaptureFromCam('')
		self.camPhoto = self.cam.read()
		return self.camPhoto
	def camReadCv(self):
		if self.cam == None:
			self.cam = cv2.VideoCapture()
			#~ self.cam = CaptureFromCam()
			#~ self.cam.open(0)
		if self.cam.isOpened() == False:
			#~ self.cam.open("http://192.168.1.104/asp/video.cgi?.mjpeg")
			#~ self.cam.open("http://192.168.1.104/video.cgi")
			camsTmp = glob('/dev/video*')
			if len(camsTmp) > 0:
				self.cam.open(camsTmp[0])
				print 'camera opened'
			else:
				print 'no camera connected'
				return
		if self.cam.isOpened() == True:
			self.camPhoto = None
			ret,self.camPhoto = self.cam.read()
			#~ ret, self.camPhoto = self.cam.retrieve()
		else:
			self.camPhoto = None
			print 'cam reading failed'
	def openwindow(self):
		if self.isWinPresent == False:
			self.__init__()
	def removewindow(self):
		self.root.destroy()
		self.isWinPresent = False
		if not self.cam == None:
			self.cam.close()
	def startTimer(self):
		self.timerCommand = True
		self.timer()
	def stopTimer(self):
		self.timerCommand = False
		print 'timer stopped'
	def timer(self):
		if self.timerCommand == True:
			self.task()
			self.root.after(self.timerInterval, self.timer)
	def task(self):
		print 'timer working'
		tic = time.time()
		self.camReadV4l()
		#~ toc = time.time()
		#~ print 'camera reading time: ', toc - tic
		#~ tic = time.time()
		
		if self.camPhoto == None:
			print 'no Image read from cam'
			#~ self.stopTimer()
			#~ return
			#~ time.sleep(1)
			
			#~ self.cam.close()
			#~ time.sleep(1)
			#~ self.cam = CaptureFromCam('')
			self.timerInterval = self.timerInterval + 1
			time.sleep(self.timerInterval/1000)
			try:
				self.cam.camLink.queue_all_buffers()
			except:
				print 'que all buffers failed'
			time.sleep(self.timerInterval/1000)
			return
		else:
			self.placeImage()
			if self.timerInterval > 2:
				self.timerInterval = self.timerInterval - 1
		toc = time.time()
		print 'time taken for display', toc - tic
		
	def placeImage(self):
		#~ bard = Image.open("lena.jpg")
		#~ camPhoto = self.camPhoto
		sizeOfDispIm = tuple( np.asarray(self.camPhoto.shape)/1)
		camPhoto = cv2.resize(self.camPhoto, ( sizeOfDispIm[1], sizeOfDispIm[0] )  )  
		self.trash = camPhoto
		#~ print camPhoto.shape
		
		self.bard = Image.fromarray(self.camPhoto)
		self.bardejov = ImageTk.PhotoImage(self.bard)
		if self.label1 == None:
			self.label1 = tk.Label(self.root, image=self.bardejov)
			#~ self.label1.configure(height = camPhoto.shape[1], width = camPhoto.shape[0])
		else:
			self.label1.configure(image = self.bardejov)
		self.label1.bardejov = self.bardejov
		self.label1.place(x=0, y=0)
		#~ self.label1.height(
		#~ height=

#~ if __name__ == '__main__':
	#~ if 'cap' in locals():
		cap.removewindow()
		#~ if not cap.cam == None:
			#~ cap.cam.close()
	#~ cap = Cap()

#~ app.openwindow()
#~ app.root.mainloop()

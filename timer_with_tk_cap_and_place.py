import Tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
from glob import glob
from v4l2_capture_class import CaptureFromCam
#~ import matplotlib.pyplot as plt
import numpy as np

class TimerWithTkCapAndPlace():
	def __init__(self, oringGui, cap):
		self.timerInterval = 30
		self.timerCommand = False
		#~ self.PlaceImage = oringGui.PlaceImage
		self.oringGui = oringGui
		#~ self.root = oringGui.master
		#~ self.fun = fun
		#~ self.args = *args
		self.cap = cap
	
	def startTimer(self):
		self.timerCommand = True
		self.timer()
		print 'timerWithTKCapAndPlace started'
	def stopTimer(self):
		self.timerCommand = False
		print 'timer stopped'
	def timer(self):
		#~ if self.oringGui.timerCommand == True
		
		if self.timerCommand == True:
			self.task()
			self.oringGui.master.after(self.timerInterval, self.timer)
			#~ self.root.after(self.timerInterval, self.timer)
	def task(self):
		#~ print 'timer working'
		tic = time.time()
		camPhoto = self.cap.camReadV4l()
		#~ toc = time.time()
		#~ print 'camera reading time: ', toc - tic
		#~ tic = time.time()
		
		if self.cap.camPhoto == None:
			print 'no Image read from cam'
			self.timerInterval = self.timerInterval + 1
			time.sleep(self.timerInterval/1000)
			try:
				self.cap.cam.camLink.queue_all_buffers()
			except:
				print 'que all buffers failed'
			time.sleep(self.timerInterval/1000)
			return
		else:
			#~ 0/0
			#~ tuple(np.asarray(camPhoto.shape)/2)
			shapeSmall = tuple(np.asarray(camPhoto.shape)/2)
			
			shapeSmall = shapeSmall[::-1]
			camPhotoForPlace = cv2.resize(camPhoto, shapeSmall)
			ret, camPhotoForPlaceBw = cv2.threshold(camPhotoForPlace, 80, 255, 0)
			self.camPhotoForPlaceBw = camPhotoForPlaceBw
			self.oringGui.PlaceImage(camPhotoForPlaceBw)
			if self.timerInterval > 30:
				self.timerInterval = self.timerInterval - 1
		toc = time.time()
		print 'time taken for display', toc - tic
		

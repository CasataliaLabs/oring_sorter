import Tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
from glob import glob
from v4l2_capture_class import CaptureFromCam
#~ import matplotlib.pyplot as plt
import numpy as np

class TimerWithTk():
	def __init__(self, root, fun, *args):
		self.timerInterval = 8
		self.timerCommand = False
		self.root = root
		self.fun = fun
		self.args = *args
	
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
		

import Tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
from glob import glob
from v4l2_capture_class import CaptureFromCam
#~ import matplotlib.pyplot as plt
import numpy as np
from oring_calc import OringCalc

class TimerContourDraw():
	def __init__(self, oringGui, cap):
		self.timerInterval = 50
		self.timerCommand = False
		#~ self.PlaceImage = oringGui.PlaceImage
		self.oringGui = oringGui
		#~ self.root = oringGui.master
		#~ self.fun = fun
		#~ self.args = *args
		self.cap = cap
		self.oringCalc = OringCalc()
	
	def startTimer(self):
		self.timerCommand = True
		self.timer()
		print 'timer Contour Running'
	def stopTimer(self):
		self.timerCommand = False
		print 'timer Contour stopped'
	def timer(self):
		#~ if self.oringGui.timerCommand == True
		
		if self.timerCommand == True:
			self.task()
			self.oringGui.root.after(self.timerInterval, self.timer)
			#~ self.root.after(self.timerInterval, self.timer)
	def task(self):
		print 'timer contour working'
		tic = time.time()
		camPhoto = self.cap.camPhoto
		#~ camPhoto = self.cap.camReadV4l()
		#~ toc = time.time()
		#~ print 'camera reading time: ', toc - tic
		#~ tic = time.time()
		time.sleep(20/1000)
		if camPhoto == None:
			camPhoto = self.cap.camReadV4l()
		time.sleep(20/1000)
		if camPhoto == None:
			camPhoto = self.cap.cam.read()
			print 'no Image in cap - message from Contour Draw'
			return
		elif camPhoto.mean() < 230:
			print 'hand in picture - message from Contour Draw'
			return
		else:
			#~ 0/0
			self.contourImage = self.oringCalc.showContour(camPhoto)
			shapeSmall = tuple(np.asarray(self.contourImage.shape)/2)
			shapeSmall = shapeSmall[::-1]
			camPhotoForPlace = cv2.resize(self.contourImage, shapeSmall)
			self.oringGui.PlaceContour(camPhotoForPlace)
			if self.timerInterval > 2:
				self.timerInterval = self.timerInterval - 1
		toc = time.time()
		print 'time taken for display', toc - tic
		

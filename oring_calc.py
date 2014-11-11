__author__ = 'sreeram'
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.cm as cm
import tkMessageBox as MessageBox 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import time
from v4l2_capture_class import CaptureFromCam
from PIL import ImageTk, Image
import os
import matplotlib.cm as cm

class OringCalc():

	def __init__(self):
		pass
		
	def showFrame(self):
		tic = time.time()
		if self.frame == None:
			print 'no frame in showFrame'
			return
		ret, imBw = cv2.threshold(self.frame,127,255,0)
		self.imBw = imBw
		tic = time.time()
		frameForDisplay = cv2.resize(self.frame, tuple((np.asarray(self.frame.shape))/10))
		self.hIm.set_data(frameForDisplay)
		#~ self.hIm.set_data(self.frame)
		canvasShowFrame.draw()
		#~ figureShowFrame.canvas.draw()
		toc = time.time()
		data = {'1': {'Time': '{0:.3f}'.format(toc - tic)}}
		model = table.model
		model.importDict(data)
		table.redrawTable()
		#~ toc = time.time()
		#~ print toc - tic

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
		
		absoluteValueOuter=self.filteredOutput.max()
		#~ absoluteValueOuter = np.sum(absoluteValueOuter * 1)
		print absoluteValueOuter
		return self.filteredOutput,absoluteValueOuter
	
	def BwConverter(self, camPhoto):
		ret, self._imBwOfBg = cv2.threshold(camPhoto, 200,1,cv2.THRESH_BINARY_INV)
		self._tmpIm = self._imBwOfBg * camPhoto
		self._threshCalculated = (self._tmpIm.max() + self._tmpIm.min())
		
		
	def showContour(self, camPhoto):
		tic = time.time()
		self.contourMinLen = 100
		self.AreaOfBackGroundContour = []
		self.bwThresh = 150
		#~ if cf.mean() < 230:
			#~ return None
		ret, imBw = cv2.threshold(camPhoto, self.bwThresh, 255,cv2.THRESH_BINARY)
		
		self.imBwTmp = imBw
		self.imBwTmp = self.imBwTmp * 1
		self.imBw = imBw
		
		contours, hierarchy = cv2.findContours(self.imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		self.contours = contours
		self.hierarchy = hierarchy
		bgImageForContourPlot = np.zeros(self.imBw.shape)
		
		beginHierarchy = hierarchy[0,0,:]
		level0 = 0
		while level0 != -1:
			level1 = hierarchy[0,level0,2]
			while level1 != -1:
				level2 = hierarchy[0,level1,2]
				if len(contours[level1]) > self.contourMinLen:
					level2 = hierarchy[0,level1,2]
					radius,angle = self.oringRadius(contours[level1])
					filteredOutput, absoluteValueOuter = self.medfilt1(radius)
					if (absoluteValueOuter > 4) or (level2 == -1):
						cv2.drawContours(bgImageForContourPlot, contours, level1, (255,0,0), -1)
					else:
						cv2.drawContours(bgImageForContourPlot, contours, level1, (255,0,0), 2)
				level1 = hierarchy[0,level1,0]

				while level2 != -1:
					level3 = hierarchy[0,level2,2]
					if len(contours[level2]) > self.contourMinLen:
						radius,angle = self.oringRadius(contours[level2])
						filteredOutput, absoluteValueOuter = self.medfilt1(radius)
						if (absoluteValueOuter > 4) or (level3 == -1):
							cv2.drawContours(bgImageForContourPlot, contours, level2, (255,0,0), -1)
						else:
							cv2.drawContours(bgImageForContourPlot, contours, level2, (255,0,0), 2)
					level2 = hierarchy[0,level2,0]
						
					while level3 != -1:
						level4 = hierarchy[0,level3,2]
						if len(contours[level3]) > self.contourMinLen:
							radius,angle = self.oringRadius(contours[level3])
							filteredOutput, absoluteValueOuter = self.medfilt1(radius)
							if (absoluteValueOuter > 4) or (level4 == -1):
								cv2.drawContours(bgImageForContourPlot, contours, level3, (255,0,0), -1)
							else:
								cv2.drawContours(bgImageForContourPlot, contours, level3, (255,0,0), 2)
						level3 = hierarchy[0,level3,0]
						#~ print 'level3'
							
						while level4 != -1:
							#~ level5 = hierarchy[0,level4,2]
							if len(contours[level4]) > self.contourMinLen:
								radius,angle = self.oringRadius(contours[level4])
								filteredOutput, absoluteValueOuter = self.medfilt1(radius)
								if (absoluteValueOuter > 4):
									cv2.drawContours(bgImageForContourPlot, contours, level4, (255,0,0), -1)
								else:
									cv2.drawContours(bgImageForContourPlot, contours, level4, (255,0,0), 2)
							level4 = hierarchy[0,level4,0]
								#~ print 'test', level4
			level0 = hierarchy[0,level0, 0]
		toc = time.time()
		print toc-tic
		self.bgImageForContourPlot = bgImageForContourPlot
		return bgImageForContourPlot
		
if __name__ == '__main__':
	oringCalc = OringCalc()
	cf = mainOring.cap.camReadV4l()
	oringCalc.showContour(cf)
	plt.subplot(221)
	#~ mainOring.oringGui.PlaceImage(cf)
	plt.imshow(oringCalc.imBwTmp, cm.gray)

	plt.subplot(223)
	plt.imshow(oringCalc.bgImageForContourPlot, cm.gray)
	#~ mainOring.oringGui.PlaceContour(oringCalc.bgImageForContourPlot)

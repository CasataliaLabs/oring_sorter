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
		self.AreaOfBackGroundContour = []
		#~ if cf.mean() < 230:
			#~ return None
		ret, imBw = cv2.threshold(camPhoto, 100,255,cv2.THRESH_BINARY)
		
		self.imBwTmp = imBw
		self.imBwTmp = self.imBwTmp * 1
		self.imBw = imBw
		
		contours, hierarchy = cv2.findContours(self.imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		self.contours = contours
		self.hierarchy = hierarchy
		bgImageForContourPlot = np.zeros(self.imBw.shape)
		self.parent = hierarchy[0,:,3]
		#~ print "hierarchy",hierarchy
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
		#~ print "outer area",self.AreaOfContourOuter
			if self.AreaOfContourOuter > 10000:
				#~ print "list of",list(self.parent).count(self.IndexOfZeroParentOuter[iterationOuter])			
				if list(self.parent).count(self.IndexOfZeroParentOuter[iterationOuter])==1:
					radius,angle = self.oringRadius(contours[self.IndexOfZeroParentOuter[iterationOuter]])
					filteredOutput, absoluteValueOuter = self.medfilt1(radius)
					#~ print "abs value",absoluteValueOuter
					if absoluteValueOuter > 4:
						cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter],(255,0,0),-1)
					else:
						cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter], 255, 2)
						
						innerContourIndex = list(self.parent).index(self.IndexOfZeroParentOuter[iterationOuter])
						innerContour = contours[innerContourIndex]
						
						radiusInner,angleInner = self.oringRadius(innerContour)
						filteredOutput, absoluteValueOuter = self.medfilt1(radiusInner)
						if absoluteValueOuter > 4:
							cv2.drawContours(bgImageForContourPlot, contours,innerContourIndex,(255,0,0),-1)
						else:
							cv2.drawContours(bgImageForContourPlot, contours,innerContourIndex,255,2) 
				else:
					
					cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter],(255,0,0),-1)		
					print 'line 138'
			else:
				
				cv2.drawContours(bgImageForContourPlot, contours,self.IndexOfZeroParentOuter[iterationOuter],(255,0,0),-1)	
				print 'line 141'
		
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

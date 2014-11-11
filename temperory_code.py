tic = time.time()
self.frame = self.captureDevice.read()
if self.frame == None:
	print 'camera read failed, line 140'
	#~ return
#~ if ret == 0:
	#~ print "reading from camera failed"
gray_scale = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
ret, imBw = cv2.threshold(gray_scale,127,255,0)
#~ gray_scale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#~ ret,thresh = cv2.threshold(frame_gray1,0,255, 128) #cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(imBw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
bgImageForContourPlot = np.zeros(imBw.shape)
cv2.drawContours(bgImageForContourPlot, contours, 1, (255,0,0), 2)
hIm = plt.imshow(bgImageForContourPlot, cmap=cm.Greys_r)

#~ 
#~ if len(contours) >= 0:
	#~ for k in range(0, len(contours)):
		#~ print k
		

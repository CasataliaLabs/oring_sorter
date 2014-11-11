import Image
import select
import v4l2capture
import numpy as np
import matplotlib.pyplot as plt
import os as os
import time
plt.ion()
from glob import glob as glob
import sys
from timer_with_tk_cap_and_place import TimerWithTkCapAndPlace
from timer_contour_draw import TimerContourDraw
from gui_for_oring import OringGUI
from cap_ import Cap

	
class MainOring():
	def __init__(self):
		self.oringGui = OringGUI()
		self.cap = Cap()
		self.timerWithTkCapAndPlace = TimerWithTkCapAndPlace(self.oringGui, self.cap)
		self.timerContourDraw = TimerContourDraw(self.oringGui, self.cap)
		self.oringGui._InitMenubar(self)
		#~ self.timeCap.startTimer()


if __name__ == '__main__':
	if 'mainOring' in locals():
		if mainOring.oringGui._isWinPresent:
			try:
				#~ mainOring.oringGui.RemoveWindow()
				pass
			except:
				print 'remove window faile'
		try:	
			#~ mainOring.cap.cam.close()
			pass
		except:
			print 'no camera'
	mainOring = MainOring()
	try:
		print '__IPYTHON__ = ',  __IPYTHON__
	except:
		mainOring.oringGui.master.mainloop()
	


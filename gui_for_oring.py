__author__ = 'kake'
import cv2
import matplotlib.pyplot as plt
import numpy as np
#~ import sys
import matplotlib.cm as cm
import Tkinter as tk
#~ from Tkinter import Tk, Menu
#~ from Tkinter import *
import tkMessageBox
#~ from repeated_timer1 import RepeatedTimer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import time
from v4l2_capture_class import CaptureFromCam
from PIL import ImageTk, Image
import os

plt.ion()

class OringGUI():
	def __init__(self):
		self._isWinPresent = False
		self.OpenWindow()
		#~ self._InitMenubar()
		self.labelIm = None
		self.labelContour = None
		self.timerCommand = False
		
	def _InitMainWindow(self):
		self.root = tk.Tk()
		self.root.withdraw()
		master = tk.Toplevel()
		master.title("Drishtiman O-Ring Sorter")
		screenWidth=master.winfo_screenwidth()
		screenHeight=master.winfo_screenheight()
		master.geometry(("%dx%d")%(screenWidth,screenHeight))
		master.protocol('WM_DELETE_WINDOW', self.RemoveWindow)
		self.master = master

	def OpenWindow(self):
		if self._isWinPresent == False:
			#~ self.__init__()
			self._InitMainWindow()
			self._isWinPresent = True

	def RemoveWindow(self):
		self.root.destroy()
		self.master.destroy()
		self._isWinPresent = False
		self.root.quit()
		self.master.quit()
		#~ if not self.cam == None:
			#~ self.cam.close()



	def _InitMenubar(self, mainObject):
		self.mainObject = mainObject
		master = self.master
		menubar = tk.Menu(master)
		filemenu = tk.Menu(menubar, tearoff=0)
		menubar.add_command(label="Run", command=self.StartButtonCommand)
		menubar.add_command(label="Stop", command=self.StopButtonCommand) # correct later
		master.config(menu=menubar)
		master.bind('r', self._ShortcutRun)
		master.bind('s', self._ShortcutStop)
		self.master = master
	
	def _ShortcutRun(self, event):
		self.StartButtonCommand()
		
	def _ShortcutStop(self, event):
		self.StopButtonCommand()
		
	def StartButtonCommand(self):
		self.mainObject.timerWithTkCapAndPlace.startTimer()
		self.mainObject.timerContourDraw.startTimer()
		print 'timer started'

	def StopButtonCommand(self):
		self.mainObject.timerWithTkCapAndPlace.stopTimer()
		self.mainObject.timerContourDraw.stopTimer()
		print 'timer stoped'
		
	def _initHelpMenu(self):
		#~ help menu
		helpmenu = Menu(menubar, tearoff=False)
		helpmenu.add_command(label="Help Docs",command=hello)
		helpmenu.add_command(label="About",command=about)
		menubar.add_cascade(label="Help",menu=helpmenu)
		master.config(menu=menubar)

	def PlaceImage(self, camPhoto):
		self._im = Image.fromarray(camPhoto)
		self._imTk = ImageTk.PhotoImage(self._im)
		if self.labelIm == None:
			self.labelIm = tk.Label(self.master, image=self._imTk)
		else:
			self.labelIm.configure(image = self._imTk)
		self.labelIm._imTk = self._imTk
		self.labelIm.place(x=0, y=0)
	
	def PlaceContour(self, im):
		self._imContour = Image.fromarray(im)
		self._imTkContour = ImageTk.PhotoImage(self._imContour)
		if self.labelContour == None:
			self.labelContour = tk.Label(self.master, image=self._imTkContour)
		else:
			self.labelContour.configure(image = self._imTkContour)
		self.labelContour._imTkContour = self._imTkContour
		self.labelContour.place(x=650, y=0)


if __name__ == '__main__':
	if 'oringGui' in locals():
		if oringGui._isWinPresent == True:
			oringGui.RemoveWindow()
	oringGui = OringGUI()

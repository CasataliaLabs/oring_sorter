__author__ = 'sreeram'
import cv2
import pylab
import numpy as np
import sys
from Tkinter import *
from repeatedTimer1 import RepeatedTimer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

#Creating window with title and geometry
master = Tk()
master.title("Oring GUI")
master.geometry("1000x1000")

#Creating figure for showing video frame
f1 = Figure(figsize=(4, 4), dpi=100)
axis1 = f1.add_subplot(111)
f1.suptitle("Live Video")

#Creating canvass for placing video frame
canvas1 = FigureCanvasTkAgg(f1, master=master)
canvas1.get_tk_widget().place(x=10, y=20)

#Capturing video frame
cap = cv2.VideoCapture(1)
gray_1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
# defining axis from the figures
x_codnte = pylab.arange(0, 100, 1)
y_codnte = pylab.array([0] * 100)

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
manager = pylab.get_current_fig_manager()
values = [0 for x in range(100)]

# table creation
frame_value = Frame(master)
frame_value.pack()
frame_value.place(x=175, y=500, width=175, height=70)
model = TableModel()
table = TableCanvas(frame_value, model=model, editable=False)
table.createTableFrame()

#Function for the acquiring values for plotting the frame variations
def frame(arg):
    global gray_1, values
    CurrentXAxis = pylab.arange(len(values) - 100, len(values), 1)
    line1[0].set_data(CurrentXAxis, pylab.array(values[-100:]))
    ax.axis([CurrentXAxis.min(), CurrentXAxis.max() + 1, 0, 255])
    manager.canvas.draw()
    pylab.draw()
    canvas2.show()

#Function to display video frame,mean of frame variations,display in a table
def video():
    global gray_1, axis1
    axis1.imshow(cap.read()[1])
    canvas1.show()
    gray_2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    frm_diff = cv2.absdiff(gray_1, gray_2)
    mean = np.mean(frm_diff)
    values.append(mean)
    data = {'1': {'Mean Value': '{0:.3f}'.format(mean)}}
    model = table.model
    model.importDict(data)
    table.redrawTable()
    values.remove(values[0])
    #gray_2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    gray_1 = gray_2

    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()

#Function for starting timers
def video_start():
    timer.start()
    t.start()

#Function for stopping timers
def video_stop():
    timer.stop()
    t.stop()

#Timer for frame
timer = f2.canvas.new_timer(interval=10)
timer.add_callback(frame, ())

#Timer for video
t = RepeatedTimer(0.01, video)

#Start and Stop Buttons
b1 = Button(master, text="Start", bg='white', command=video_start).place(x=50, y=600)
b2 = Button(master, text="Stop", bg='white', command=video_stop).place(x=400, y=600)
master.mainloop()


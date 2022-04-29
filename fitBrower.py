from glob import glob
import fitdecode
import matplotlib.pylab as plt
from matplotlib.widgets import Cursor
from matplotlib.widgets import MultiCursor
from matplotlib.backend_bases import MouseButton

f=fitdecode.FitReader('trainer.fit')
records=[]
laps=[]

for frame in f:
    if isinstance(frame, fitdecode.records.FitDataMessage):
        if frame.name=='lab':
            laps.append(frame)     
        elif frame.name == 'record':
            records.append(frame)


fields=[]
for fieldN in records[0].fields:
    if fieldN.name.find('unknown') == -1:
        fields.append(fieldN.name)

print(fields)

hr=[]
power=[]

for frame in records:
    if frame.has_field('heart_rate'):
        hr.append(frame.get_value('heart_rate'))
    if frame.has_field('power'):
        power.append(frame.get_value('power'))



fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.plot(hr)
ax2.plot(power)

ax1Area=None

pressed=False
xStart=0
def on_press(event):
    global pressed
    global xStart
    global ax1Area
    del(ax1Area)
    if event.inaxes:
        if event.button is MouseButton.LEFT:
            ax1Area=event.inaxes.axvspan(xStart, xStart,0,10000,alpha=0.5, color='red')
            print("press")
            xStart=event.x
            print(xStart)
            pressed=True

def on_release(event):
    global pressed
    if event.inaxes:
        if event.button is MouseButton.LEFT:
            print("release")
            pressed=False

def on_move(event):
    global pressed
    global ax1
    global xStart
    if pressed==True:
        x, y = event.x, event.y
        if event.inaxes:
            #axtemp = event.inaxes  # the axes instance
            ax1Area.set_xy([[0,100],[0,100]])
            print('data coords %f %f' % (event.xdata, event.ydata))
            



plt.connect('button_press_event', on_press)
plt.connect('button_release_event', on_release)
binding_id = plt.connect('motion_notify_event', on_move)

#ax1.axvspan(8, 14, alpha=0.5, color='red')
plt.show()

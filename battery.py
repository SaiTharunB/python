import tkinter
from tkinter import messagebox as mb
import psutil
b=psutil.sensors_battery()
def fun():
 per=b.percent
 plug=b.power_plugged
 if(per>=89 and plug):
  mb.showinfo("Battery","Battery is {0} unplug the charger".format(per))
 if(per<=35 and not plug):
  mb.showinfo("Battery","Battery is {0} plug the charger".format(per))
fun()
#!/usr/bin/python

import wx
from Adafruit_I2C import Adafruit_I2C as I2C
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time


ADC.setup()
PWM.start("P9_14",50,500,0)

class MyFrame(wx.Frame):
	def __init__(self,parent,id,title):
		wx.Frame.__init__(self,parent,id,title,wx.DefaultPosition,(300,500))
		panel = wx.Panel(self, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.sldx = wx.Slider(panel, -1, 200, 0, 1024, wx.DefaultPosition, (250, -1), wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		self.sldy = wx.Slider(panel, -1, 200, 0, 1024, wx.DefaultPosition, (250, -1), wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		self.sldz = wx.Slider(panel, -1, 200, 0, 1024, wx.DefaultPosition, (250, -1), wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		btn1 = wx.Button(panel, 8, 'Adjust')
		btn2 = wx.Button(panel, 9, 'Close')
	
		wx.EVT_BUTTON(self, 8, self.OnAdjust)
		wx.EVT_BUTTON(self, 9, self.OnClose)
		vbox.Add(self.sldx, 1, wx.ALIGN_CENTRE)
		vbox.Add(self.sldy, 1, wx.ALIGN_CENTRE)
		vbox.Add(self.sldz, 1, wx.ALIGN_CENTRE)
		hbox.Add(btn1,1,wx.RIGHT,10)
		hbox.Add(btn2,1)
		vbox.Add(hbox,0,wx.ALIGN_CENTRE | wx.ALL, 20)
		panel.SetSizer(vbox)
	
	def OnAdjust(self,event):
		#val = self.sld.GetValue()
		#self.SetSize((val*2,val))
		valuex1 = acc.readU8(0x32)
                valuex2 = acc.readU8(0x33)
                valuex = (valuex2 << 8) + valuex1
                if valuex > (1<<15):
                        valuex = int(bin(valuex),2)-(1<<16)
                #print (bin(value),2)
                print "val %i, val1: %i, val2: %i\n" % (valuex, valuex1, valuex2)
                PWM.set_duty_cycle("P9_14",((valuex+512.0)/1024.0)*100.0)
			


		valuey1 = acc.readU8(0x34)
                valuey2 = acc.readU8(0x35)
                valuey = (valuey2 << 8) + valuey1
                if valuey > (1<<15):
                        valuey = int(bin(valuey),2)-(1<<16)

		valuez1 = acc.readU8(0x36)
                valuez2 = acc.readU8(0x37)
                valuez = (valuez2 << 8) + valuez1
                if valuez > (1<<15):
                        valuez = int(bin(valuez),2)-(1<<16)

		self.sldx.SetValue(valuex+512)
		self.sldy.SetValue(valuey+512)
		self.sldz.SetValue(valuez+512)

	def OnClose(self,event):
		self.Close()

class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None,-1,"foo")
		frame.Show(True)
		frame.Centre()
		return True

acc = I2C(0x53)
acc.write8(0x31,0xB)
acc.write8(0x2d,0x8)
acc.write8(0x2e,0x80)
app = MyApp(0)
app.MainLoop()

#app = wx.App()

#frame = wx.Frame(None,-1, 'accelerometer')
#panel = wx.Panel(self, -1)

#slider = wxSlider(
#frame.Show()

#app.MainLoop()

#while 1:
#def MainLoop():
#	value = ADC.read("P9_40")
#	PWM.set_duty_cycle("P9_14",value*100.0)
#	str(value)
#	time.sleep(.01)


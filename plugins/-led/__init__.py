#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
	import RPi.GPIO as GPIO
	from playsound import playsound as _playsound
	
	ledgpiopin=18
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(ledgpiopin,GPIO.OUT)
	
	def playsound(path):
		if path.endswith("beep.ogg"):
			GPIO.output(ledgpiopin,GPIO.HIGH)
		elif path.endswith("peeb.ogg"):
			GPIO.output(ledgpiopin,GPIO.LOW)
		_playsound(path)
except:
	pass
import time
#from rpi_ws281x import *
#
## LED strip configuration:
#LED_COUNT      = 26      # Number of LED pixels.
#LED_PIN        = 18      # GPIO pin connected to the pixels (18 ses PWM!).
##LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
#LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
#LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
#LED_BRIGHTNESS = 60     # Set to 0 for darkest and 255 for brightest
#LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
#LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#
## Create NeoPixel object with appropriate configuration.
#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#
#strip.begin()
#
#for i in range(10):
#	strip.setPixelColor(i, Color(255, 0, 0))
#	if i > 0:
#		strip.setPixelColor(i - 1, Color(0, 0, 0))
#	strip.show()
#	time.sleep(1)
#for i in range(strip.numPixels()):
#	strip.setPixelColor(i, Color(0,255,0))
#strip.show()
#time.sleep(3)
#for i in range(strip.numPixels()):
#	strip.setPixelColor(i, Color(0,0,0))
#strip.show()
	
#for j in range(0,8,1):
#	for q in range(0,32,1):
#		for i in range(0,8,1):
#			for r in range(-2, 3, 1):
#				#print(q-i+(r*16))
#				strip.setPixelColor(q-i+(r*16), Color(255, 0, 0))
#		strip.show()
#		time.sleep(40.0/1000.0)
#		#time.sleep(1)
#		for i in range(0,8,1):
#			for r in range(-2, 3, 1):
#				#print(q-i+(r*16))
#				strip.setPixelColor(q-i+(r*16), Color(0,0,0))
#for i in range(strip.numPixels()):
#	strip.setPixelColor(i, Color(0,0,0))
#	strip.show()

import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 26, brightness=0.1)

#pixels[0] = (255, 0, 0)
def ledtest():
	for i in range(10):
		pixels[i] = (255, 0, 0)
		if i > 0:
			pixels[i-1] = (0, 0, 0)
		time.sleep(1)
	pixels.fill((0, 255, 0))
	time.sleep(3)
	pixels.fill((0, 0, 0))

ledtest()
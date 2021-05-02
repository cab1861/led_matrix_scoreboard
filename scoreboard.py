from render import ScoreboardData
import time, api_pull, data_fill#, led_strip
#import board
#import neopixel
#strip = neopixel.NeoPixel(board.D10, 26, brightness=.5)
#
##strip[0] = (255, 0, 0)
#for i in range(10):
#	strip[i] = (255, 0, 0)
#	if i > 0:
#		strip[i-1] = (0, 0, 0)
#	time.sleep(1)
#
#strip.fill((0, 0, 0))
#led_strip.ledtest()

while True:
	
	#ScoreboardData.display_clock()
	api_pull.nhl_preferred_request()
	data_fill.nhl_preferred_dump()
	
	
	if ScoreboardData.nhl_preferred_playing == False:
		api_pull.nhl_request()
		data_fill.nhl_dump()
		
		api_pull.nfl_request()
		data_fill.nfl_dump()

		api_pull.nwhl_request()
		data_fill.nwhl_dump()

		api_pull.ritmhky_request()
		data_fill.ritmhky_dump()

		api_pull.ritwhky_request()
		data_fill.ritwhky_dump()

		api_pull.nascar_request()
		data_fill.nascar_dump()
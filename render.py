import requests
import json
import time
import pytz
import re

from datetime import date, datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw, ImageFont

# Get timezones set up and todays date
utc = pytz.utc
eastern = pytz.timezone('US/Eastern')
now = date.today()
today = now.strftime("%b %-d")
#time_now = now.strftime("%-I:%M%p")

class ScoreboardData:
	nhl_root_location = "https://statsapi.web.nhl.com/api/v1/"
	fontpath = "fonts/"
	imagepath = "logos/"
	
	schedule_date = ""
	schedule_time = ""
	game_count = 0
	current_game = 0
	nhl_preferred_data = ""
	nhl_preferred_playing = ""
	nhl_data = ""
	nfl_data = ""
	nwhl_data = ""
	ritmhky_data = ""
	ritwhky_data = ""
	nascar_data = ""
	race_id = ""
	series = ""
	status = ""
	game_type = ""
	game_day = ""
	game_time = ""
	home_id = 0
	home_team = ""
	home_pullgoalie = ""
	home_icestrength = 0
	home_haspowerplay = ""
	away_id = 0
	away_team = ""
	away_pullgoalie = ""
	away_icestrength = 0
	away_haspowerplay = ""
	current_period = ""
	game_clock = ""
	game_score = ""
	current_possession = ""
	red_zone = ""
	series_name = ""
	race_time = ""
	track = ""
	
	#sets text
	Timefont = fontpath + "Large.ttf"
	Scorefont = fontpath + "Medium.ttf"
	Clockfont = fontpath + "Medium.ttf"
	Textfont = fontpath + "Small.ttf"
	textRed = (255, 0, 0)
	textWhite = (255, 255, 255)
	textYellow = (255, 255, 0)
	textGreen = (0, 255, 0)
	fnt = ImageFont.truetype(Scorefont, 10)
	fnt2 = ImageFont.truetype(Textfont, 8)
	fnt3 = ImageFont.truetype(Clockfont, 10)
	fnt4 = ImageFont.truetype(Timefont, 12)
	
	# Configuration for the matrix
	options = RGBMatrixOptions()
	options.cols = 128
	options.rows = 32
	options.hardware_mapping = 'adafruit-hat-pwm'
	options.brightness = 40

	matrix = RGBMatrix(options = options)
	canvas = matrix.CreateFrameCanvas()
	
	matrix.Clear()
	canvas.Clear()
	
	# CLOCK DISPLAY
	
	def display_clock():
		print("Clock")
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Initiate textboxes
		time_box = Image.new("RGB", (25, 12), (0, 0, 0))
		draw_time_box = ImageDraw.Draw(time_box)
		seconds_box = Image.new("RGB", (10, 6), (0, 0, 0))
		draw_seconds_box = ImageDraw.Draw(seconds_box)
		
		#for i in range(5):
		current_time = datetime.now()
		time_now = current_time.strftime("%-I:%M")
		seconds = current_time.strftime("%S")
		
		draw_time_box.text((0, 0), time_now, font=ScoreboardData.fnt4, fill=ScoreboardData.textRed)
		draw_seconds_box.text((0, 0), seconds, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		
		# Make image fit our screen.
		time_box.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		seconds_box.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)

		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(time_box.convert('RGB'), 40, 0)
		ScoreboardData.matrix.SetImage(seconds_box.convert('RGB'), 65, 6)

		time.sleep(1)
	
	# STARTUP TITLE DISPLAYS
	
	def nhl_start_display():
		print("NHL Scoreboard")
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Render team logos for the matrix
		logo = Image.open(ScoreboardData.imagepath + "nhl/NHL.png")
		title = "NHL SCORES"
		game_list = str(ScoreboardData.game_count) + " GAMES"
		
		# Initiate textboxes
		text = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_text = ImageDraw.Draw(text)
		date = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_date = ImageDraw.Draw(date)
		games = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_games = ImageDraw.Draw(games)
		
		title_size = 0
		date_size = 0
		games_size = 0
		for character in title:
			if character == "I" or character == "T" or character == "1":
				title_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				title_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				title_size += 2
			elif character == "," or character == " ":
				title_size += 3
			else:
				title_size += 5	
		title_offset = (text.size[0] // 2) - ((title_size - 1) // 2)
		
		for character in ScoreboardData.schedule_date:
			if character == "I" or character == "T" or character == "1":
				date_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				date_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				date_size += 2
			elif character == "," or character == " ":
				date_size += 3
			else:
				date_size += 5	
		date_offset = (date.size[0] // 2) - ((date_size - 1) // 2)
		
		for character in game_list:
			if character == "I" or character == "T" or character == "1":
				games_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				games_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				games_size += 2
			elif character == "," or character == " ":
				games_size += 3
			else:
				games_size += 5	
		games_offset = (games.size[0] // 2) - ((games_size - 1) // 2)
		
		draw_text.text((title_offset, 0), title, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
		draw_date.text((date_offset, 0), ScoreboardData.schedule_date, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_games.text((games_offset, 0), game_list, font=ScoreboardData.fnt2, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		logo.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		text.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		date.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		games.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(logo.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(text.convert('RGB'), 40, 0)
		ScoreboardData.matrix.SetImage(date.convert('RGB'), 40, 11)
		ScoreboardData.matrix.SetImage(games.convert('RGB'), 40, 23)
		time.sleep(3)
	
	def nfl_start_display():
		print("NFL Scoreboard")
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Render team logos for the matrix
		logo = Image.open(ScoreboardData.imagepath + "nfl/NFL.png")
		
		title = "NFL SCORES"
		game_list = str(ScoreboardData.game_count)
		
		
		# Initiate textboxes
		text = Image.new("RGB", (88, 8), (0, 0, 0))
		draw_text = ImageDraw.Draw(text)
		date = Image.new("RGB", (88, 19), (0, 0, 0))
		draw_date = ImageDraw.Draw(date)
		
		title_size = 0
		date_size = 0
		games_size = 0
		for character in title:
			if character == "I" or character == "T" or character == "1":
				title_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				title_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				title_size += 2
			elif character == "," or character == " ":
				title_size += 3
			else:
				title_size += 5	
		title_offset = (text.size[0] // 2) - ((title_size - 1) // 2)
		
		for character in ScoreboardData.schedule_date:
			if character == "I" or character == "T" or character == "1":
				date_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				date_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				date_size += 2
			elif character == "," or character == " ":
				date_size += 3
			else:
				date_size += 5
		if "Conference" in ScoreboardData.schedule_date:
			date_offset = 13
		else:
			date_offset = (date.size[0] // 2) - ((date_size - 1) // 2)
		
		draw_text.text((title_offset, 0), title, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
		draw_date.text((date_offset, 0), ScoreboardData.schedule_date, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		
		# Make image fit our screen.
		logo.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		text.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		date.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(logo.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(text.convert('RGB'), 40, 0)
		ScoreboardData.matrix.SetImage(date.convert('RGB'), 40, 11)

		time.sleep(3)
	
	def nwhl_start_display():
		print("NWHL Scoreboard")
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Render team logos for the matrix
		logo = Image.open(ScoreboardData.imagepath + "nwhl/NWHL.png")
		title = "NWHL SCORES"
		#game_list = str(ScoreboardData.game_count) + " GAMES"
		game_list = ""
		ScoreboardData.schedule_date = today
		
		# Initiate textboxes
		text = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_text = ImageDraw.Draw(text)
		date = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_date = ImageDraw.Draw(date)
		games = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_games = ImageDraw.Draw(games)
		
		title_size = 0
		date_size = 0
		games_size = 0
		for character in title:
			if character == "I" or character == "T" or character == "1":
				title_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				title_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				title_size += 2
			elif character == "," or character == " ":
				title_size += 3
			else:
				title_size += 5	
		title_offset = (text.size[0] // 2) - ((title_size - 1) // 2)
		
		for character in ScoreboardData.schedule_date:
			if character == "I" or character == "T" or character == "1":
				date_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				date_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				date_size += 2
			elif character == "," or character == " ":
				date_size += 3
			else:
				date_size += 5	
		date_offset = (date.size[0] // 2) - ((date_size - 1) // 2)
		
		for character in game_list:
			if character == "I" or character == "T" or character == "1":
				games_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				games_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				games_size += 2
			elif character == "," or character == " ":
				games_size += 3
			else:
				games_size += 5	
		games_offset = (games.size[0] // 2) - ((games_size - 1) // 2)
		
		draw_text.text((title_offset, 0), title, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
		draw_date.text((date_offset, 0), ScoreboardData.schedule_date, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_games.text((games_offset, 0), game_list, font=ScoreboardData.fnt2, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		logo.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		text.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		date.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		games.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(logo.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(text.convert('RGB'), 40, 0)
		ScoreboardData.matrix.SetImage(date.convert('RGB'), 40, 11)
		ScoreboardData.matrix.SetImage(games.convert('RGB'), 40, 23)
		time.sleep(3)
	
	def ncaamhcky_start_display():
		print("NCAA Scoreboard")
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Render team logos for the matrix
		logo = Image.open(ScoreboardData.imagepath + "college/NCAA.png")
		title = "NCAA MHCKY SCORES"
		#game_list = str(ScoreboardData.game_count) + " GAMES"
		game_list = ""
		ScoreboardData.schedule_date = today
		
		# Initiate textboxes
		text = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_text = ImageDraw.Draw(text)
		date = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_date = ImageDraw.Draw(date)
		games = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_games = ImageDraw.Draw(games)
		
		title_size = 0
		date_size = 0
		games_size = 0
		for character in title:
			if character == "I" or character == "T" or character == "1":
				title_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				title_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				title_size += 2
			elif character == "," or character == " ":
				title_size += 3
			else:
				title_size += 5	
		title_offset = (text.size[0] // 2) - ((title_size - 1) // 2)
		
		for character in ScoreboardData.schedule_date:
			if character == "I" or character == "T" or character == "1":
				date_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				date_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				date_size += 2
			elif character == "," or character == " ":
				date_size += 3
			else:
				date_size += 5	
		date_offset = (date.size[0] // 2) - ((date_size - 1) // 2)
		
		for character in game_list:
			if character == "I" or character == "T" or character == "1":
				games_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				games_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				games_size += 2
			elif character == "," or character == " ":
				games_size += 3
			else:
				games_size += 5	
		games_offset = (games.size[0] // 2) - ((games_size - 1) // 2)
		
		draw_text.text((title_offset, 0), title, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
		draw_date.text((date_offset, 0), ScoreboardData.schedule_date, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_games.text((games_offset, 0), game_list, font=ScoreboardData.fnt2, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		logo.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		text.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		date.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		games.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(logo.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(text.convert('RGB'), 40, 0)
		ScoreboardData.matrix.SetImage(date.convert('RGB'), 40, 11)
		ScoreboardData.matrix.SetImage(games.convert('RGB'), 40, 23)
		time.sleep(3)
	
	def ncaawhcky_start_display():
		print("NCAA Scoreboard")
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Render team logos for the matrix
		logo = Image.open(ScoreboardData.imagepath + "college/NCAA.png")
		title = "NCAA WHCKY SCORES"
		#game_list = str(ScoreboardData.game_count) + " GAMES"
		game_list = ""
		ScoreboardData.schedule_date = today
		
		# Initiate textboxes
		text = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_text = ImageDraw.Draw(text)
		date = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_date = ImageDraw.Draw(date)
		games = Image.new("RGB", (88, 7), (0, 0, 0))
		draw_games = ImageDraw.Draw(games)
		
		title_size = 0
		date_size = 0
		games_size = 0
		for character in title:
			if character == "I" or character == "T" or character == "1":
				title_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				title_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				title_size += 2
			elif character == "," or character == " ":
				title_size += 3
			else:
				title_size += 5	
		title_offset = (text.size[0] // 2) - ((title_size - 1) // 2)
		
		for character in ScoreboardData.schedule_date:
			if character == "I" or character == "T" or character == "1":
				date_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				date_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				date_size += 2
			elif character == "," or character == " ":
				date_size += 3
			else:
				date_size += 5	
		date_offset = (date.size[0] // 2) - ((date_size - 1) // 2)
		
		for character in game_list:
			if character == "I" or character == "T" or character == "1":
				games_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				games_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				games_size += 2
			elif character == "," or character == " ":
				games_size += 3
			else:
				games_size += 5	
		games_offset = (games.size[0] // 2) - ((games_size - 1) // 2)
		
		draw_text.text((title_offset, 0), title, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
		draw_date.text((date_offset, 0), ScoreboardData.schedule_date, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_games.text((games_offset, 0), game_list, font=ScoreboardData.fnt2, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		logo.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		text.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		date.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		games.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(logo.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(text.convert('RGB'), 40, 0)
		ScoreboardData.matrix.SetImage(date.convert('RGB'), 40, 11)
		ScoreboardData.matrix.SetImage(games.convert('RGB'), 40, 23)
		time.sleep(3)
	

	# SCOREBOARDS
	
	def nascar_start_display():
		# Render team logos for the matrix
		logo = Image.open(ScoreboardData.imagepath + "nascar/NASCAR.png")
		#home = Image.open(ScoreboardData.imagepath + "nhl/NTH.png")
		
		# Initiate textboxes
		series_title = Image.new("RGB", (64, 8), (0, 0, 0))
		draw_series_title = ImageDraw.Draw(series_title)
		date = Image.new("RGB", (64, 7), (0, 0, 0))
		draw_date = ImageDraw.Draw(date)
		racetime = Image.new("RGB", (64, 7), (0, 0, 0))
		draw_racetime = ImageDraw.Draw(racetime)
		games = Image.new("RGB", (128, 8), (0, 0, 0))
		draw_games = ImageDraw.Draw(games)
		
		title_size = 0
		date_size = 0
		time_size = 0
		games_size = 0
		for character in ScoreboardData.series_name:
			if character == "I" or character == "T" or character == "1":
				title_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				title_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				title_size += 2
			elif character == "," or character == " ":
				title_size += 3
			else:
				title_size += 5	
		title_offset = (series_title.size[0] // 2) - ((title_size - 1) // 2)
		
		for character in ScoreboardData.schedule_date:
			if character == "I" or character == "T" or character == "1":
				date_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				date_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				date_size += 2
			elif character == "," or character == " ":
				date_size += 3
			else:
				date_size += 5	
		date_offset = (date.size[0] // 2) - ((date_size - 1) // 2)
		
		for character in ScoreboardData.race_time:
			if character == "I" or character == "T" or character == "1":
				time_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				time_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				time_size += 2
			elif character == "," or character == " ":
				time_size += 3
			else:
				time_size += 5	
		time_offset = (racetime.size[0] // 2) - ((time_size - 1) // 2)
		
		for character in ScoreboardData.track:
			if character == "I" or character == "T" or character == "1":
				games_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				games_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				games_size += 2
			elif character == "," or character == " ":
				games_size += 3
			else:
				games_size += 5	
		games_offset = (games.size[0] // 2) - ((games_size - 1) // 2)
		
		draw_series_title.text((title_offset, 0), ScoreboardData.series_name, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
		draw_date.text((date_offset, 0), ScoreboardData.schedule_date, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_racetime.text((time_offset, 0), ScoreboardData.race_time, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_games.text((games_offset, 0), ScoreboardData.track, font=ScoreboardData.fnt2, fill=ScoreboardData.textYellow)
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Make image fit our screen.
		logo.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		series_title.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		date.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		racetime.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		games.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(logo.convert('RGB'), 0, -3)
		ScoreboardData.matrix.SetImage(series_title.convert('RGB'), 64, 0)
		ScoreboardData.matrix.SetImage(date.convert('RGB'), 64, 9)
		ScoreboardData.matrix.SetImage(racetime.convert('RGB'), 64, 17)
		ScoreboardData.matrix.SetImage(games.convert('RGB'), 0, 24)
		
		time.sleep(3)
	
	
	# DISPLAY SCOREBOARDS
	
	
	def nhl_display_scores():
		# API Calls for team logos
		r = requests.get(ScoreboardData.nhl_root_location + "teams/")
		data = r.json()
		for teams in data["teams"]:
			if teams["id"] == ScoreboardData.home_id:
				ScoreboardData.home_team = teams["abbreviation"]
			elif teams["id"] == ScoreboardData.away_id:
				ScoreboardData.away_team = teams["abbreviation"]
		#print(ScoreboardData.game_time + " - " + ScoreboardData.status + ": " + ScoreboardData.current_period + " " + ScoreboardData.game_clock)
		#print(str(ScoreboardData.home_team) + " vs " + str(ScoreboardData.away_team) + ", " + ScoreboardData.game_score)
		
		# Render team logos for the matrix
		home = Image.open(ScoreboardData.imagepath + "nhl/" + ScoreboardData.home_team + ".png")
		away = Image.open(ScoreboardData.imagepath + "nhl/" + ScoreboardData.away_team + ".png")

		# Initiate textboxes for time, scores & indicators
		clock = Image.new("RGB", (34, 11), (0, 0, 0))
		draw_clock = ImageDraw.Draw(clock)
		
		#period = Image.new("RGB", (34, 6), (0, 0, 10))
		period = Image.new("RGB", (46, 6), (0, 0, 0))
		draw_period = ImageDraw.Draw(period)
		
		score = Image.new("RGB", (34, 10), (0, 0, 0))
		draw_score = ImageDraw.Draw(score)
		
		home_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		draw_home_powerplay = ImageDraw.Draw(home_powerplay)
		away_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		draw_away_powerplay = ImageDraw.Draw(away_powerplay)
		
		game_scroll = Image.new("RGB", (48, 1), (0, 0, 0))
		draw_game_scroll = ImageDraw.Draw(game_scroll)
		
		# Draw Game Scroller
		current_indicator = 0
		indicator_offset = 24 - ((ScoreboardData.game_count * 2) // 2)
		for position in range(0, ScoreboardData.game_count * 2, 2):
			if current_indicator == ScoreboardData.current_game:
				draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textRed)
			else:
				draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textWhite)
			current_indicator += 1
		
		# Game Postponed changes text color
		if ScoreboardData.status == "Scheduled" or ScoreboardData.status == "Pre-Game" or ScoreboardData.status == "Final" or ScoreboardData.status == "Game Over" or ScoreboardData.status == "Postponed":
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		elif "INT" in ScoreboardData.game_clock:
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		
		# On ice strength indicators
		if ScoreboardData.home_pullgoalie == True:
			draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textGreen)
			if ScoreboardData.home_haspowerplay == True:
				if ScoreboardData.away_icestrength == 4:
					draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textYellow)
				elif ScoreboardData.away_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
					draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
		
		elif ScoreboardData.away_pullgoalie == True:
			draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textGreen)
			if ScoreboardData.away_haspowerplay == True:
				if ScoreboardData.home_icestrength == 4:
					draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textYellow)
				elif ScoreboardData.home_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
					draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)
		else:
			if ScoreboardData.home_haspowerplay == True:
				if ScoreboardData.away_icestrength == 4:
					draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
				elif ScoreboardData.away_icestrength == 3: 
					draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
					if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
						draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
			if ScoreboardData.away_haspowerplay == True:
				if ScoreboardData.home_icestrength == 4:
					draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
				elif ScoreboardData.home_icestrength == 3:
					draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
					if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
						draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)		

		# Text Offset
		clock_size = 0
		period_size = 0
		score_size = 0
		for character in ScoreboardData.game_clock:
			if ":" in ScoreboardData.game_clock:
				if character == ":" or character == "." or character == " ":
					clock_size += 3
				elif character == "-":
					clock_size += 5
				else:
					clock_size += 7
			else:
				if character == "I" or character == "T" or character == "1":
					clock_size += 4
				elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
					clock_size += 6
				elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
					clock_size += 2
				elif character == "," or character == " ":
					clock_size += 3
				else:
					clock_size += 5
		clock_offset = (clock.size[0] // 2) - ((clock_size - 1) // 2)
		
		for character in ScoreboardData.current_period:
			if character == "I" or character == "T" or character == "1":
				period_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				period_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				period_size += 2
			elif character == "," or character == " ":
				period_size += 3
			else:
				period_size += 5	
		period_offset = (period.size[0] // 2) - ((period_size - 1) // 2)
		
		for character in ScoreboardData.game_score:
			if character == ":" or character == "." or character == " ":
				score_size += 3
			elif character == "-":
				score_size += 5
			else:
				score_size += 7
		score_offset = (score.size[0] // 2) - ((score_size - 1) // 2)
		
		# Adjust text color if game is postponed
		if ScoreboardData.current_period == "POSTPONED":
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
			ScoreboardData.game_score = ""
		else:
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_clock.text((clock_offset, 0), ScoreboardData.game_clock, font=ScoreboardData.fnt3, fill=ScoreboardData.textRed)
		draw_score.text((score_offset, 0), ScoreboardData.game_score, font=ScoreboardData.fnt, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		home.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		score.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		clock.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		period.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		home_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		game_scroll.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Sets next display
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(home.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(away.convert('RGB'), (128-away.size[0]), 0)
		ScoreboardData.matrix.SetImage(score.convert('RGB'), 47, 20)
		ScoreboardData.matrix.SetImage(clock.convert('RGB'), 47, 0)
		#ScoreboardData.matrix.SetImage(period.convert('RGB'), 47, 11)
		ScoreboardData.matrix.SetImage(period.convert('RGB'), 41, 11)
		ScoreboardData.matrix.SetImage(home_powerplay.convert('RGB'), 41, 22)
		ScoreboardData.matrix.SetImage(away_powerplay.convert('RGB'), 80, 22)
		ScoreboardData.matrix.SetImage(game_scroll.convert('RGB'), 40, 31)
		
		time.sleep(5)
		
		# Resets text
		ScoreboardData.fnt = ImageFont.truetype(ScoreboardData.Scorefont, 10)
		ScoreboardData.fnt2 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Clockfont, 10)
		ScoreboardData.current_game += 1
		
	def nfl_display_scores():
		#print("Hi")
		
		#print(ScoreboardData.game_time + " - " + ScoreboardData.status + ": " + ScoreboardData.current_period + " " + ScoreboardData.game_clock)
		
		#print(str(ScoreboardData.home_team) + " vs " + str(ScoreboardData.away_team) + ", " + ScoreboardData.game_score)
		
		# Render team logos for the matrix
		home = Image.open(ScoreboardData.imagepath + "nfl/" + ScoreboardData.home_team + ".png")
		away = Image.open(ScoreboardData.imagepath + "nfl/" + ScoreboardData.away_team + ".png")
		
		# Initiate textboxes for time, scores & indicators
		score = Image.new("RGB", (34, 10), (0, 0, 0))
		draw_score = ImageDraw.Draw(score)
		clock = Image.new("RGB", (34, 11), (0, 0, 0))
		draw_clock = ImageDraw.Draw(clock)
		#period = Image.new("RGB", (34, 6), (0, 0, 0))
		period = Image.new("RGB", (46, 6), (0, 0, 0))
		draw_period = ImageDraw.Draw(period)
		home_possession = Image.new("RGB", (7, 7), (0, 0, 0))
		draw_home_possession = ImageDraw.Draw(home_possession)
		away_possession= Image.new("RGB", (7, 7), (0, 0, 0))
		draw_away_possession = ImageDraw.Draw(away_possession)
		
		game_scroll = Image.new("RGB", (48, 1), (0, 0, 0))
		draw_game_scroll = ImageDraw.Draw(game_scroll)
		
		# Draw Game Scroller
		current_indicator = 0
		indicator_offset = 24 - ((ScoreboardData.game_count * 2) // 2)
		for position in range(0, ScoreboardData.game_count * 2, 2):
			if current_indicator == ScoreboardData.current_game:
				draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textRed)
			else:
				draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textWhite)
			current_indicator += 1
		
		if ScoreboardData.status == "Scheduled":
			if ScoreboardData.game_day == today:
				ScoreboardData.game_clock = "TODAY"
			else:
				ScoreboardData.game_clock = ScoreboardData.game_day
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
			ScoreboardData.current_period = ScoreboardData.game_time
			ScoreboardData.game_score = ""
		elif ScoreboardData.status == "In Progress":
			# Draw Possession Indicator
			if ScoreboardData.current_possession == ScoreboardData.home_id:
				draw_home_possession.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
				if ScoreboardData.red_zone:
					draw_home_possession.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
			elif ScoreboardData.current_possession == ScoreboardData.away_id:
				draw_away_possession.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
				if ScoreboardData.red_zone:
					draw_away_possession.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)
		elif ScoreboardData.status == "End of Period":
			ScoreboardData.current_period = "End " + ScoreboardData.current_period
		elif ScoreboardData.status == "Halftime":
			ScoreboardData.game_clock = "HALF"
			ScoreboardData.current_period = ""
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		elif ScoreboardData.status == "Final":
			ScoreboardData.game_clock = "FINAL"
			if ScoreboardData.current_period != "OT":
				ScoreboardData.current_period = ""
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		elif ScoreboardData.status == "Canceled":
			ScoreboardData.game_clock = ""
			ScoreboardData.current_period = "CANCELED"
			ScoreboardData.game_score = ""
		elif ScoreboardData.status == "Postponed":
			ScoreboardData.game_clock = ""
			ScoreboardData.current_period = "POSTPONED"
			ScoreboardData.game_score = ""
		else:
			ScoreboardData.current_period = ScoreboardData.status
		
		# Text Offset
		clock_size = 0
		period_size = 0
		score_size = 0
		for character in ScoreboardData.game_clock:
			if ":" in ScoreboardData.game_clock:
				if character == ":" or character == "." or character == " ":
					clock_size += 3
				elif character == "-":
					clock_size += 5
				else:
					clock_size += 7
			else:
				if character == "I" or character == "T" or character == "1":
					clock_size += 4
				elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
					clock_size += 6
				elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
					clock_size += 2
				elif character == "," or character == " ":
					clock_size += 3
				else:
					clock_size += 5
		clock_offset = (clock.size[0] // 2) - ((clock_size - 1) // 2)
		
		for character in ScoreboardData.current_period:
			if character == "I" or character == "T" or character == "1":
				period_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				period_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				period_size += 2
			elif character == "," or character == " ":
				period_size += 3
			else:
				period_size += 5	
		period_offset = (period.size[0] // 2) - ((period_size - 1) // 2)
		
		for character in ScoreboardData.game_score:
			if character == ":" or character == "." or character == " ":
				score_size += 3
			elif character == "-":
				score_size += 5
			else:
				score_size += 7
		score_offset = (score.size[0] // 2) - ((score_size - 1) // 2)
		
		if ScoreboardData.current_period == "CANCELED" or ScoreboardData.current_period == "POSTPONED":
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
			ScoreboardData.game_score = ""
		else:
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_clock.text((clock_offset, 0), ScoreboardData.game_clock, font=ScoreboardData.fnt3, fill=ScoreboardData.textRed)
		draw_score.text((score_offset, 0), ScoreboardData.game_score, font=ScoreboardData.fnt, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		home.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		score.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		clock.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		period.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		home_possession.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away_possession.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		game_scroll.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Sets next display
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(home.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(away.convert('RGB'), (128-away.size[0]), 0)
		ScoreboardData.matrix.SetImage(score.convert('RGB'), 47, 20)
		ScoreboardData.matrix.SetImage(clock.convert('RGB'), 47, 0)
		#ScoreboardData.matrix.SetImage(period.convert('RGB'), 47, 11)
		ScoreboardData.matrix.SetImage(period.convert('RGB'), 41, 11)
		ScoreboardData.matrix.SetImage(home_possession.convert('RGB'), 41, 22)
		ScoreboardData.matrix.SetImage(away_possession.convert('RGB'), 80, 22)
		ScoreboardData.matrix.SetImage(game_scroll.convert('RGB'), 40, 31)
		
		time.sleep(5)
		
		# Resets text
		ScoreboardData.fnt = ImageFont.truetype(ScoreboardData.Scorefont, 10)
		ScoreboardData.fnt2 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Clockfont, 10)
		ScoreboardData.current_game += 1
		
	def nwhl_display_games():
		# Render team logos for the matrix
		home = Image.open(ScoreboardData.imagepath + "nwhl/" + ScoreboardData.home_team + ".png")
		away = Image.open(ScoreboardData.imagepath + "nwhl/" + ScoreboardData.away_team + ".png")

		# Initiate textboxes for time, scores & indicators
		clock = Image.new("RGB", (34, 11), (0, 0, 0))
		draw_clock = ImageDraw.Draw(clock)
		
		#period = Image.new("RGB", (34, 6), (0, 0, 10))
		period = Image.new("RGB", (46, 6), (0, 0, 0))
		draw_period = ImageDraw.Draw(period)
		
		#score = Image.new("RGB", (34, 10), (0, 0, 0))
		#draw_score = ImageDraw.Draw(score)
		
		#home_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		#draw_home_powerplay = ImageDraw.Draw(home_powerplay)
		#away_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		#draw_away_powerplay = ImageDraw.Draw(away_powerplay)
		
		#game_scroll = Image.new("RGB", (48, 1), (0, 0, 0))
		#draw_game_scroll = ImageDraw.Draw(game_scroll)
		
		# Draw Game Scroller
		#current_indicator = 0
		#indicator_offset = 24 - ((ScoreboardData.game_count * 2) // 2)
		#for position in range(0, ScoreboardData.game_count * 2, 2):
		#	if current_indicator == ScoreboardData.current_game:
		#		draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textRed)
		#	else:
		#		draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textWhite)
		#	current_indicator += 1
		
		# Game Postponed changes text color
		#if ScoreboardData.status == "Scheduled" or ScoreboardData.status == "Pre-Game" or ScoreboardData.status == "Final" or ScoreboardData.status == "Game Over" or ScoreboardData.status == "Postponed":
		#	ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		#elif "INT" in ScoreboardData.game_clock:
		#	ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		
		# On ice strength indicators
		#if ScoreboardData.home_pullgoalie == True:
		#	draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textGreen)
		#	if ScoreboardData.home_haspowerplay == True:
		#		if ScoreboardData.away_icestrength == 4:
		#			draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.away_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
		#			draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
		
		#elif ScoreboardData.away_pullgoalie == True:
		#	draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textGreen)
		#	if ScoreboardData.away_haspowerplay == True:
		#		if ScoreboardData.home_icestrength == 4:
		#			draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.home_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
		#			draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)
		#else:
		#	if ScoreboardData.home_haspowerplay == True:
		#		if ScoreboardData.away_icestrength == 4:
		#			draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.away_icestrength == 3: 
		#			draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
		#			if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
		#				draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
		#	if ScoreboardData.away_haspowerplay == True:
		#		if ScoreboardData.home_icestrength == 4:
		#			draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.home_icestrength == 3:
		#			draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
		#			if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
		#				draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)		
		ScoreboardData.game_clock = ScoreboardData.game_day
		ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		ScoreboardData.current_period = ScoreboardData.game_time
		
		# Text Offset
		clock_size = 0
		period_size = 0
		#score_size = 0
		for character in ScoreboardData.game_clock:
			if ":" in ScoreboardData.game_clock:
				if character == ":" or character == "." or character == " ":
					clock_size += 3
				elif character == "-":
					clock_size += 5
				else:
					clock_size += 7
			else:
				if character == "I" or character == "T" or character == "1":
					clock_size += 4
				elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
					clock_size += 6
				elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
					clock_size += 2
				elif character == "," or character == " ":
					clock_size += 3
				else:
					clock_size += 5
		clock_offset = (clock.size[0] // 2) - ((clock_size - 1) // 2)
		
		for character in ScoreboardData.current_period:
			if character == "I" or character == "T" or character == "1":
				period_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				period_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				period_size += 2
			elif character == "," or character == " ":
				period_size += 3
			else:
				period_size += 5	
		period_offset = (period.size[0] // 2) - ((period_size - 1) // 2)
		
		#for character in ScoreboardData.game_score:
		#	if character == ":" or character == "." or character == " ":
		#		score_size += 3
		#	elif character == "-":
		#		score_size += 5
		#	else:
		#		score_size += 7
		#score_offset = (score.size[0] // 2) - ((score_size - 1) // 2)
		
		# Adjust text color if game is postponed
		#if ScoreboardData.current_period == "POSTPONED":
		#	draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
		#	ScoreboardData.game_score = ""
		#else:
		#	draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_clock.text((clock_offset, 0), ScoreboardData.game_clock, font=ScoreboardData.fnt3, fill=ScoreboardData.textRed)
		#draw_score.text((score_offset, 0), ScoreboardData.game_score, font=ScoreboardData.fnt, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		home.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#score.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		clock.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		period.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#home_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#game_scroll.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Sets next display
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(home.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(away.convert('RGB'), (128-away.size[0]), 0)
		#ScoreboardData.matrix.SetImage(score.convert('RGB'), 47, 20)
		ScoreboardData.matrix.SetImage(clock.convert('RGB'), 47, 0)
		ScoreboardData.matrix.SetImage(period.convert('RGB'), 41, 11)
		#ScoreboardData.matrix.SetImage(home_powerplay.convert('RGB'), 41, 22)
		#ScoreboardData.matrix.SetImage(away_powerplay.convert('RGB'), 80, 22)
		#ScoreboardData.matrix.SetImage(game_scroll.convert('RGB'), 40, 31)
		
		time.sleep(5)
		
		# Resets text
		ScoreboardData.fnt = ImageFont.truetype(ScoreboardData.Scorefont, 10)
		ScoreboardData.fnt2 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Clockfont, 10)
		#ScoreboardData.current_game += 1
	
	def ritmhky_display_scores():
		# Render team logos for the matrix
		home = Image.open(ScoreboardData.imagepath + "college/" + ScoreboardData.home_team + ".png")
		away = Image.open(ScoreboardData.imagepath + "college/" + ScoreboardData.away_team + ".png")

		# Initiate textboxes for time, scores & indicators
		clock = Image.new("RGB", (34, 11), (0, 0, 0))
		draw_clock = ImageDraw.Draw(clock)
		
		#period = Image.new("RGB", (34, 6), (0, 0, 10))
		period = Image.new("RGB", (46, 6), (0, 0, 0))
		draw_period = ImageDraw.Draw(period)
		
		score = Image.new("RGB", (34, 10), (0, 0, 0))
		draw_score = ImageDraw.Draw(score)
		
		#home_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		#draw_home_powerplay = ImageDraw.Draw(home_powerplay)
		#away_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		#draw_away_powerplay = ImageDraw.Draw(away_powerplay)
		
		#game_scroll = Image.new("RGB", (48, 1), (0, 0, 0))
		#draw_game_scroll = ImageDraw.Draw(game_scroll)
		
		# Draw Game Scroller
		#current_indicator = 0
		#indicator_offset = 24 - ((ScoreboardData.game_count * 2) // 2)
		#for position in range(0, ScoreboardData.game_count * 2, 2):
		#	if current_indicator == ScoreboardData.current_game:
		#		draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textRed)
		#	else:
		#		draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textWhite)
		#	current_indicator += 1
		
		# Game Postponed changes text color
		if ScoreboardData.status == "Scheduled" or ScoreboardData.status == "Pre-Game" or ScoreboardData.status == "Final" or ScoreboardData.status == "Game Over" or ScoreboardData.status == "Postponed" or ScoreboardData.status == "Canceled":
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		elif "INT" in ScoreboardData.game_clock:
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		
		# On ice strength indicators
		#if ScoreboardData.home_pullgoalie == True:
		#	draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textGreen)
		#	if ScoreboardData.home_haspowerplay == True:
		#		if ScoreboardData.away_icestrength == 4:
		#			draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.away_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
		#			draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
		
		#elif ScoreboardData.away_pullgoalie == True:
		#	draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textGreen)
		#	if ScoreboardData.away_haspowerplay == True:
		#		if ScoreboardData.home_icestrength == 4:
		#			draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.home_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
		#			draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)
		#else:
		#	if ScoreboardData.home_haspowerplay == True:
		#		if ScoreboardData.away_icestrength == 4:
		#			draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.away_icestrength == 3: 
		#			draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
		#			if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
		#				draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
		#	if ScoreboardData.away_haspowerplay == True:
		#		if ScoreboardData.home_icestrength == 4:
		#			draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.home_icestrength == 3:
		#			draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
		#			if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
		#				draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)		
		#ScoreboardData.game_clock = ScoreboardData.game_day
		#ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		#ScoreboardData.current_period = ScoreboardData.game_time
		
		# Text Offset
		clock_size = 0
		period_size = 0
		score_size = 0
		for character in ScoreboardData.game_clock:
			if ":" in ScoreboardData.game_clock:
				if character == ":" or character == "." or character == " ":
					clock_size += 3
				elif character == "-":
					clock_size += 5
				else:
					clock_size += 7
			else:
				if character == "I" or character == "T" or character == "1":
					clock_size += 4
				elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
					clock_size += 6
				elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
					clock_size += 2
				elif character == "," or character == " ":
					clock_size += 3
				else:
					clock_size += 5
		clock_offset = (clock.size[0] // 2) - ((clock_size - 1) // 2)
		
		for character in ScoreboardData.current_period:
			if character == "I" or character == "T" or character == "1":
				period_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				period_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				period_size += 2
			elif character == "," or character == " ":
				period_size += 3
			else:
				period_size += 5	
		period_offset = (period.size[0] // 2) - ((period_size - 1) // 2)
		
		for character in ScoreboardData.game_score:
			if character == ":" or character == "." or character == " ":
				score_size += 3
			elif character == "-":
				score_size += 5
			else:
				score_size += 7
		score_offset = (score.size[0] // 2) - ((score_size - 1) // 2)
		
		# Adjust text color if game is postponed
		if ScoreboardData.current_period == "CANCELED" or ScoreboardData.current_period == "POSTPONED":
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
			ScoreboardData.game_score = ""
		else:
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		#draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_clock.text((clock_offset, 0), ScoreboardData.game_clock, font=ScoreboardData.fnt3, fill=ScoreboardData.textRed)
		draw_score.text((score_offset, 0), ScoreboardData.game_score, font=ScoreboardData.fnt, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		home.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		score.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		clock.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		period.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#home_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#game_scroll.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Sets next display
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(home.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(away.convert('RGB'), (128-away.size[0]), 0)
		ScoreboardData.matrix.SetImage(score.convert('RGB'), 47, 20)
		ScoreboardData.matrix.SetImage(clock.convert('RGB'), 47, 0)
		ScoreboardData.matrix.SetImage(period.convert('RGB'), 41, 11)
		#ScoreboardData.matrix.SetImage(home_powerplay.convert('RGB'), 41, 22)
		#ScoreboardData.matrix.SetImage(away_powerplay.convert('RGB'), 80, 22)
		#ScoreboardData.matrix.SetImage(game_scroll.convert('RGB'), 40, 31)
		
		time.sleep(5)
		
		# Resets text
		ScoreboardData.fnt = ImageFont.truetype(ScoreboardData.Scorefont, 10)
		ScoreboardData.fnt2 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Clockfont, 10)
		#ScoreboardData.current_game += 1
	
	def ritwhky_display_scores():
		# Render team logos for the matrix
		home = Image.open(ScoreboardData.imagepath + "college/" + ScoreboardData.home_team + ".png")
		away = Image.open(ScoreboardData.imagepath + "college/" + ScoreboardData.away_team + ".png")

		# Initiate textboxes for time, scores & indicators
		clock = Image.new("RGB", (34, 11), (0, 0, 0))
		draw_clock = ImageDraw.Draw(clock)
		
		#period = Image.new("RGB", (34, 6), (0, 0, 10))
		period = Image.new("RGB", (46, 6), (0, 0, 0))
		draw_period = ImageDraw.Draw(period)
		
		score = Image.new("RGB", (34, 10), (0, 0, 0))
		draw_score = ImageDraw.Draw(score)
		
		#home_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		#draw_home_powerplay = ImageDraw.Draw(home_powerplay)
		#away_powerplay = Image.new("RGB", (7, 7), (0, 0, 0))
		#draw_away_powerplay = ImageDraw.Draw(away_powerplay)
		
		#game_scroll = Image.new("RGB", (48, 1), (0, 0, 0))
		#draw_game_scroll = ImageDraw.Draw(game_scroll)
		
		# Draw Game Scroller
		#current_indicator = 0
		#indicator_offset = 24 - ((ScoreboardData.game_count * 2) // 2)
		#for position in range(0, ScoreboardData.game_count * 2, 2):
		#	if current_indicator == ScoreboardData.current_game:
		#		draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textRed)
		#	else:
		#		draw_game_scroll.line((position + indicator_offset, 0, position + indicator_offset, 0),fill=ScoreboardData.textWhite)
		#	current_indicator += 1
		
		# Game Postponed changes text color
		if ScoreboardData.status == "Scheduled" or ScoreboardData.status == "Pre-Game" or ScoreboardData.status == "Final" or ScoreboardData.status == "Game Over" or ScoreboardData.status == "Postponed" or ScoreboardData.status == "Canceled":
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		elif "INT" in ScoreboardData.game_clock:
			ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		
		# On ice strength indicators
		#if ScoreboardData.home_pullgoalie == True:
		#	draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textGreen)
		#	if ScoreboardData.home_haspowerplay == True:
		#		if ScoreboardData.away_icestrength == 4:
		#			draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.away_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
		#			draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
		
		#elif ScoreboardData.away_pullgoalie == True:
		#	draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textGreen)
		#	if ScoreboardData.away_haspowerplay == True:
		#		if ScoreboardData.home_icestrength == 4:
		#			draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.home_icestrength == 3 and ("OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P"):
		#			draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)
		#else:
		#	if ScoreboardData.home_haspowerplay == True:
		#		if ScoreboardData.away_icestrength == 4:
		#			draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.away_icestrength == 3: 
		#			draw_home_powerplay.line((5,1,3,3,5,5),fill=ScoreboardData.textYellow)
		#			if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
		#				draw_home_powerplay.line((3,1,1,3,3,5),fill=ScoreboardData.textRed)
		#	if ScoreboardData.away_haspowerplay == True:
		#		if ScoreboardData.home_icestrength == 4:
		#			draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
		#		elif ScoreboardData.home_icestrength == 3:
		#			draw_away_powerplay.line((1,1,3,3,1,5),fill=ScoreboardData.textYellow)
		#			if "OT" not in ScoreboardData.current_period or ScoreboardData.game_type == "P":
		#				draw_away_powerplay.line((3,1,5,3,3,5),fill=ScoreboardData.textRed)		
		#ScoreboardData.game_clock = ScoreboardData.game_day
		#ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		#ScoreboardData.current_period = ScoreboardData.game_time
		
		# Text Offset
		clock_size = 0
		period_size = 0
		score_size = 0
		for character in ScoreboardData.game_clock:
			if ":" in ScoreboardData.game_clock:
				if character == ":" or character == "." or character == " ":
					clock_size += 3
				elif character == "-":
					clock_size += 5
				else:
					clock_size += 7
			else:
				if character == "I" or character == "T" or character == "1":
					clock_size += 4
				elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
					clock_size += 6
				elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
					clock_size += 2
				elif character == "," or character == " ":
					clock_size += 3
				else:
					clock_size += 5
		clock_offset = (clock.size[0] // 2) - ((clock_size - 1) // 2)
		
		for character in ScoreboardData.current_period:
			if character == "I" or character == "T" or character == "1":
				period_size += 4
			elif character == "M" or character == "N" or character == "Q" or character == "U" or character == "V" or character == "W" or character == "X" or character == "Y" or character == "m" or character == "q" or character == "u" or character == "v" or character == "w" or character == "x":
				period_size += 6
			elif character == "i" or character == "l" or character == "Q" or character == "U" or character == "." or character == ":":
				period_size += 2
			elif character == "," or character == " ":
				period_size += 3
			else:
				period_size += 5	
		period_offset = (period.size[0] // 2) - ((period_size - 1) // 2)
		
		for character in ScoreboardData.game_score:
			if character == ":" or character == "." or character == " ":
				score_size += 3
			elif character == "-":
				score_size += 5
			else:
				score_size += 7
		score_offset = (score.size[0] // 2) - ((score_size - 1) // 2)
		
		# Adjust text color if game is postponed
		if ScoreboardData.current_period == "CANCELED" or ScoreboardData.current_period == "POSTPONED":
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textRed)
			ScoreboardData.game_score = ""
		else:
			draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		#draw_period.text((period_offset, 0), ScoreboardData.current_period, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
		draw_clock.text((clock_offset, 0), ScoreboardData.game_clock, font=ScoreboardData.fnt3, fill=ScoreboardData.textRed)
		draw_score.text((score_offset, 0), ScoreboardData.game_score, font=ScoreboardData.fnt, fill=ScoreboardData.textYellow)
		
		# Make image fit our screen.
		home.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		away.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		score.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		clock.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		period.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#home_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		#game_scroll.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
		
		# Clears previous display
		ScoreboardData.matrix.Clear()
		
		# Sets next display
		# Offset coordinates (x, y)
		ScoreboardData.matrix.SetImage(home.convert('RGB'), 0, 0)
		ScoreboardData.matrix.SetImage(away.convert('RGB'), (128-away.size[0]), 0)
		ScoreboardData.matrix.SetImage(score.convert('RGB'), 47, 20)
		ScoreboardData.matrix.SetImage(clock.convert('RGB'), 47, 0)
		ScoreboardData.matrix.SetImage(period.convert('RGB'), 41, 11)
		#ScoreboardData.matrix.SetImage(home_powerplay.convert('RGB'), 41, 22)
		#ScoreboardData.matrix.SetImage(away_powerplay.convert('RGB'), 80, 22)
		#ScoreboardData.matrix.SetImage(game_scroll.convert('RGB'), 40, 31)
		
		time.sleep(5)
		
		# Resets text
		ScoreboardData.fnt = ImageFont.truetype(ScoreboardData.Scorefont, 10)
		ScoreboardData.fnt2 = ImageFont.truetype(ScoreboardData.Textfont, 8)
		ScoreboardData.fnt3 = ImageFont.truetype(ScoreboardData.Clockfont, 10)
		#ScoreboardData.current_game += 1
	
	def nascar_display():
		print("NASCAR Leaderboard")
		current_time = datetime.now()
		time_now = current_time.strftime("%H:%M:%S")
		
		# Initiate textboxes for time, scores & indicators
		laps = Image.new("RGB", (64, 7), (0, 0, 0))
		draw_laps = ImageDraw.Draw(laps)
		
		leaderboard = Image.new("RGB", (64, 24), (0, 0, 0))
		draw_leaderboard = ImageDraw.Draw(leaderboard)
		
		leaderboard2 = Image.new("RGB", (64, 24), (0, 0, 0))
		draw_leaderboard2 = ImageDraw.Draw(leaderboard2)
		
		stage = Image.new("RGB", (64, 7), (0, 0, 0))
		draw_stage = ImageDraw.Draw(stage)
		print(time_now)
		try:
			# API Calls for Running Order, Laps, Flag Condition, etc.
			r = requests.get("https://cf.nascar.com/live/feeds/" + str(ScoreboardData.series) + "/" + str(ScoreboardData.race_id) + "/live_feed.json")
			data = r.json()
			
			if ScoreboardData.schedule_time < time_now:
				if data["stage"]["finish_at_lap"] == data["laps_in_race"]:
					stage_count = "FINAL STAGE"
					lap_count = str(data["laps_to_go"]) + " TO GO"
				else:
					stage_count = "STAGE " + str(data["stage"]["stage_num"])
					lap_count = "LAP: " + str(data["lap_number"]) + " OF " + str(data["laps_in_race"])
			else:
				stage_count = data["run_name"]
				lap_count = ScoreboardData.schedule_time
			
			print(stage_count)
			print(lap_count)
			
			if data["flag_state"] == 1:
				flag_state = (0, 255, 0)
			elif data["flag_state"] == 2:
				flag_state = (255, 255, 0)
			elif data["flag_state"] == 3:
				flag_state = (255, 0, 0)
			#elif data["flag_state"] == 4:
			#	print("Checkered Flag")
			#	flag_state = (255, 255, 255)
			#elif data["flag_state"] == 8:
			#	print("Pace Laps")
			#	flag_state = (255, 255, 255)
			else:
				#print("Not On Track")
				flag_state = (255, 255, 255)
			
			#if data["lap_number"] == (data["laps_in_race"] - 1) or data["flag_state"] == 4:
			#	draw_flag.rectangle((0,0,2,2),fill=(255,255,255))
			#	draw_flag.rectangle((6,0,8,2),fill=(255,255,255))
			#	draw_flag.rectangle((12,0,14,2),fill=(255,255,255))
			#	draw_flag.rectangle((3,3,5,6),fill=(255,255,255))
			#	draw_flag.rectangle((9,3,11,6),fill=(255,255,255))
			
			position = 1
			for race_stats in data["vehicles"]:
				driver = str(position) + ". " + race_stats["vehicle_number"] + " " + race_stats["driver"]["last_name"]
				#print(str(position + 1) + ". " + race_stats["vehicle_number"] + " " + race_stats["driver"]["last_name"])
				if " #" in driver:
					driver = driver.strip(" #")
					driver_text = (255, 255, 0)
					print(driver)
				elif "(i)" in driver:
					driver = driver.strip("(i)")
					driver_text = (255, 255, 255)
					print(driver)
				else:
					driver_text = (255, 255, 255)
					print(driver)
				if position <= 3:
					draw_leaderboard.text((0, ((position-1) * 8)), driver, font=ScoreboardData.fnt2, fill=driver_text)
				elif position <= 5:
					draw_leaderboard2.text((0, ((position-4) * 8)), driver, font=ScoreboardData.fnt2, fill=driver_text)
				position += 1
				
			#home_powerplay = Image.new("RGB", (7, 7), (10, 10, 0))
			#draw_home_powerplay = ImageDraw.Draw(home_powerplay)
			#away_powerplay = Image.new("RGB", (7, 7), (10, 10, 0))
			#draw_away_powerplay = ImageDraw.Draw(away_powerplay)

			# Clears previous display
			ScoreboardData.matrix.Clear()

			draw_laps.text((0, 0), lap_count, font=ScoreboardData.fnt2, fill=flag_state)
			#draw_stage.text((0, 0), stage_count, font=ScoreboardData.fnt2, fill=ScoreboardData.textWhite)
			draw_stage.text((0, 0), stage_count, font=ScoreboardData.fnt2, fill=flag_state)

			# Make image fit our screen.
			leaderboard.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
			leaderboard2.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
			stage.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
			laps.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
			#home_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
			#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)
			#away_powerplay.thumbnail((ScoreboardData.matrix.width, ScoreboardData.matrix.height), Image.ANTIALIAS)

			# Offset coordinates (x, y)
			#ScoreboardData.matrix.SetImage(home.convert('RGB'), 0, 0)
			ScoreboardData.matrix.SetImage(leaderboard.convert('RGB'), 0, 8)
			ScoreboardData.matrix.SetImage(leaderboard2.convert('RGB'), 64, 8)
			ScoreboardData.matrix.SetImage(laps.convert('RGB'), 0, 0)
			ScoreboardData.matrix.SetImage(stage.convert('RGB'), 64, 0)

			#ScoreboardData.matrix.SetImage(home_powerplay.convert('RGB'), 41, 22)
			#ScoreboardData.matrix.SetImage(away_powerplay.convert('RGB'), 80, 22)

			time.sleep(5)
		except ValueError:
			print("No Race Data Found")
		
		
		
		
		
		
		
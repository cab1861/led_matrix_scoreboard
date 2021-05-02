import time
import os
import pytz
import re
import requests

from datetime import date, datetime
from render import ScoreboardData

# Get timezones set up and todays date
utc = pytz.utc
eastern = pytz.timezone('US/Eastern')
now = date.today()
today = now.strftime("%b %-d")

def nhl_preferred_dump():
	ScoreboardData.nhl_preferred_playing = False
	for events in ScoreboardData.nhl_preferred_data["dates"]:
		if "In Progress" in events["games"][0]["status"]["detailedState"] and events["games"][0]["linescore"]["currentPeriodTimeRemaining"] != "END":
			#print("Sabres game in progress")
			ScoreboardData.nhl_preferred_playing = True
			for event in ScoreboardData.nhl_preferred_data["dates"][0]["games"]:
				# Get game status: Scheduled / Pre-Game / In Progress / In Progress - Critical / END / OT / Final
				ScoreboardData.status = event["status"]["detailedState"]
				ScoreboardData.game_type = event["gameType"]

				# Get game day and time
				date = datetime.strptime(event["gameDate"], '%Y-%m-%dT%H:%M:%SZ')
				utc_time = utc.localize(date)
				eastern_time = utc_time.astimezone(eastern)
				ScoreboardData.game_day = eastern_time.strftime('%b %-d')
				ScoreboardData.game_time = eastern_time.strftime('%-I:%M%p')

				# Get team abbreviations and id numbers
				ScoreboardData.home_id = event["teams"]["home"]["team"]["id"]
				ScoreboardData.away_id = event["teams"]["away"]["team"]["id"]

				# Get game score
				home_score = event["teams"]["home"]["score"]
				away_score = event["teams"]["away"]["score"]
				ScoreboardData.game_score = str(home_score) + "-" + str(away_score)

				# Get game clock
				if ScoreboardData.status == "Scheduled" or ScoreboardData.status == "Pre-Game":
					ScoreboardData.current_period = ScoreboardData.game_time
					ScoreboardData.game_clock = "TODAY"
					ScoreboardData.game_score = ""
				#	fnt3 = ImageFont.truetype(Textfont, 8)
				#elif ScoreboardData.status == "Pre-Game":
				#	current_period = "1st"
				#	game_clock = "20:00"
				elif ScoreboardData.status == "Postponed":
					ScoreboardData.current_period = "POSTPONED"
					ScoreboardData.game_clock = ""
				elif ScoreboardData.status == "Final" or ScoreboardData.status == "Game Over":
					ScoreboardData.current_period = ""
					if event["linescore"]["currentPeriodOrdinal"] == "3rd":
						ScoreboardData.game_clock = "FINAL"
					else:
						ScoreboardData.game_clock = "F/" + event["linescore"]["currentPeriodOrdinal"]
				else:
					ScoreboardData.current_period = event["linescore"]["currentPeriodOrdinal"]
					ScoreboardData.game_clock = event["linescore"]["currentPeriodTimeRemaining"]
					if ScoreboardData.game_clock == "END":
						ScoreboardData.game_clock = event["linescore"]["currentPeriodOrdinal"] + " INT"
						ScoreboardData.current_period = ""
					elif ScoreboardData.game_clock[0] == "0":
						ScoreboardData.game_clock = ScoreboardData.game_clock[1:]

				# Get On-ice strength, goalie pull and powerplay status
				ScoreboardData.home_pullgoalie = event["linescore"]["teams"]["home"]["goaliePulled"]
				ScoreboardData.home_icestrength = event["linescore"]["teams"]["home"]["numSkaters"]
				ScoreboardData.home_haspowerplay = event["linescore"]["teams"]["home"]["powerPlay"]
				#print("Home Strength: " + str(ScoreboardData.home_icestrength) + " Pulled? " + str(ScoreboardData.home_pullgoalie) + " Powerplay? " + str(ScoreboardData.home_haspowerplay))

				ScoreboardData.away_pullgoalie = event["linescore"]["teams"]["away"]["goaliePulled"]
				ScoreboardData.away_icestrength = event["linescore"]["teams"]["away"]["numSkaters"]
				ScoreboardData.away_haspowerplay = event["linescore"]["teams"]["away"]["powerPlay"]
				#print("Away Strength: " + str(ScoreboardData.away_icestrength) + " Pulled? " + str(ScoreboardData.away_pullgoalie) + " Powerplay? " + str(ScoreboardData.away_haspowerplay))

				ScoreboardData.nhl_display_scores()

def nhl_dump():
	# Title Page Data
	ScoreboardData.game_count = ScoreboardData.nhl_data["totalGames"]
	current_date = datetime.strptime(ScoreboardData.nhl_data["dates"][0]["date"], "%Y-%m-%d")
	ScoreboardData.schedule_date = current_date.strftime("%b %-d")
	ScoreboardData.current_game = 0
	
	if ScoreboardData.game_count != 0:
		ScoreboardData.nhl_start_display()
		
		for event in ScoreboardData.nhl_data["dates"][0]["games"]:
			# Get game status: Scheduled / Pre-Game / In Progress / In Progress - Critical / END / OT / Final
			ScoreboardData.status = event["status"]["detailedState"]
			ScoreboardData.game_type = event["gameType"]

			# Get game day and time
			date = datetime.strptime(event["gameDate"], '%Y-%m-%dT%H:%M:%SZ')
			utc_time = utc.localize(date)
			eastern_time = utc_time.astimezone(eastern)
			ScoreboardData.game_day = eastern_time.strftime('%b %-d')
			ScoreboardData.game_time = eastern_time.strftime('%-I:%M%p')

			# Get team abbreviations and id numbers
			ScoreboardData.home_id = event["teams"]["home"]["team"]["id"]
			ScoreboardData.away_id = event["teams"]["away"]["team"]["id"]

			# Get game score
			home_score = event["teams"]["home"]["score"]
			away_score = event["teams"]["away"]["score"]
			ScoreboardData.game_score = str(home_score) + "-" + str(away_score)

			# Get game clock
			if ScoreboardData.status == "Scheduled" or ScoreboardData.status == "Pre-Game":
				ScoreboardData.current_period = ScoreboardData.game_time
				ScoreboardData.game_clock = "TODAY"
				ScoreboardData.game_score = ""
			#	fnt3 = ImageFont.truetype(Textfont, 8)
			#elif ScoreboardData.status == "Pre-Game":
			#	current_period = "1st"
			#	game_clock = "20:00"
			elif ScoreboardData.status == "Postponed":
				ScoreboardData.current_period = "POSTPONED"
				ScoreboardData.game_clock = ""
			elif ScoreboardData.status == "Final" or ScoreboardData.status == "Game Over":
				ScoreboardData.current_period = ""
				if event["linescore"]["currentPeriodOrdinal"] == "3rd":
					ScoreboardData.game_clock = "FINAL"
				else:
					ScoreboardData.game_clock = "F/" + event["linescore"]["currentPeriodOrdinal"]
			else:
				ScoreboardData.current_period = event["linescore"]["currentPeriodOrdinal"]
				ScoreboardData.game_clock = event["linescore"]["currentPeriodTimeRemaining"]
				if ScoreboardData.game_clock == "END":
					ScoreboardData.game_clock = event["linescore"]["currentPeriodOrdinal"] + " INT"
					ScoreboardData.current_period = ""
				elif ScoreboardData.game_clock[0] == "0":
					ScoreboardData.game_clock = ScoreboardData.game_clock[1:]

			# Get On-ice strength, goalie pull and powerplay status
			ScoreboardData.home_pullgoalie = event["linescore"]["teams"]["home"]["goaliePulled"]
			ScoreboardData.home_icestrength = event["linescore"]["teams"]["home"]["numSkaters"]
			ScoreboardData.home_haspowerplay = event["linescore"]["teams"]["home"]["powerPlay"]
			#print("Home Strength: " + str(ScoreboardData.home_icestrength) + " Pulled? " + str(ScoreboardData.home_pullgoalie) + " Powerplay? " + str(ScoreboardData.home_haspowerplay))

			ScoreboardData.away_pullgoalie = event["linescore"]["teams"]["away"]["goaliePulled"]
			ScoreboardData.away_icestrength = event["linescore"]["teams"]["away"]["numSkaters"]
			ScoreboardData.away_haspowerplay = event["linescore"]["teams"]["away"]["powerPlay"]
			#print("Away Strength: " + str(ScoreboardData.away_icestrength) + " Pulled? " + str(ScoreboardData.away_pullgoalie) + " Powerplay? " + str(ScoreboardData.away_haspowerplay))

			ScoreboardData.nhl_display_scores()

def nfl_dump():
	# Title Page Data
	# Get Number of Games this Week
	ScoreboardData.game_count = 0
	for event in ScoreboardData.nfl_data["events"]:
		ScoreboardData.game_count += 1
	
	# Set up Week Identifier
	if ScoreboardData.nfl_data["leagues"][0]["season"]["type"]["type"] == 1:
		ScoreboardData.schedule_date = "Preseason Week " + str(ScoreboardData.nfl_data["week"]["number"])
	elif ScoreboardData.nfl_data["leagues"][0]["season"]["type"] == 2:
		ScoreboardData.schedule_date = "Week " + str(ScoreboardData.nfl_data["week"]["number"])
	elif ScoreboardData.nfl_data["leagues"][0]["season"]["type"] == 3:
		if ScoreboardData.nfl_data["week"]["number"] == 1:
			ScoreboardData.schedule_date = "Wild Card Round"
		elif ScoreboardData.nfl_data["week"]["number"] == 2:
			ScoreboardData.schedule_date = "Divisional Round"
		elif ScoreboardData.nfl_data["week"]["number"] == 3:
			ScoreboardData.schedule_date = "  Conference\nChampionships"
		elif ScoreboardData.nfl_data["week"]["number"] == 4:
			ScoreboardData.schedule_date = "Pro Bowl"
		elif ScoreboardData.nfl_data["week"]["number"] == 5:
			ScoreboardData.schedule_date = "Super Bowl"
		else:
			ScoreboardData.schedule_date = ""
	else:
		ScoreboardData.schedule_date = "Offseason"
	ScoreboardData.current_game = 0
	
	if ScoreboardData.schedule_date != "Offseason":
		ScoreboardData.nfl_start_display()

		for event in ScoreboardData.nfl_data["events"]:
			# Get game status: Scheduled / In Progress / End of Period / Halftime / Final
			ScoreboardData.status = event["status"]["type"]["description"]

			# Get game day and time
			date = datetime.strptime(event["date"], '%Y-%m-%dT%H:%MZ')
			utc_time = utc.localize(date)
			eastern_time = utc_time.astimezone(eastern)
			ScoreboardData.game_day = eastern_time.strftime('%b %-d')
			ScoreboardData.game_time = eastern_time.strftime('%-I:%M%p')

			# Get team abbreviations and id numbers
			ScoreboardData.home_id = event["competitions"][0]["competitors"][0]["id"]
			ScoreboardData.home_team = event["competitions"][0]["competitors"][0]["team"]["abbreviation"]
			ScoreboardData.away_id = event["competitions"][0]["competitors"][1]["id"]
			ScoreboardData.away_team = event["competitions"][0]["competitors"][1]["team"]["abbreviation"]

			# Get game clock
			ScoreboardData.game_clock = event["status"]["displayClock"]

			# Get current period/quarter
			if event["status"]["period"] == 1:
				ScoreboardData.current_period = "1st"
			elif event["status"]["period"] == 2:
				ScoreboardData.current_period = "2nd"
			elif event["status"]["period"] == 3:
				ScoreboardData.current_period = "3rd"
			elif event["status"]["period"] == 4:
				ScoreboardData.current_period = "4th"
			else:
				ScoreboardData.current_period = "OT"

			# Get game score
			home_score = event["competitions"][0]["competitors"][0]["score"]
			away_score = event["competitions"][0]["competitors"][1]["score"]
			ScoreboardData.game_score = home_score + "-" + away_score

			# Get team id with possession
			if "situation" in event["competitions"][0].keys():
				if "possession" in event["competitions"][0]["situation"].keys():
					ScoreboardData.current_possession = event["competitions"][0]["situation"]["possession"]
					ScoreboardData.red_zone = event["competitions"][0]["situation"]["isRedZone"]
				else:
					ScoreboardData.current_possession = 0
					ScoreboardData.red_zone = False
			else:
				ScoreboardData.current_possession = 0
				ScoreboardData.red_zone = False



			ScoreboardData.nfl_display_scores()

def nwhl_dump():
	for event in ScoreboardData.nwhl_data.walk('VEVENT'):
		# Get game day and time
		date = datetime.strptime(str(event['DTSTART'].dt), '%Y-%m-%d %H:%M:%S%z')
		#utc_time = utc.localize(date)
		eastern_time = date.astimezone(eastern)
		ScoreboardData.game_day = eastern_time.strftime('%b %-d')
		ScoreboardData.game_time = eastern_time.strftime('%-I:%M%p')
		if ScoreboardData.game_day == today:
			ScoreboardData.nwhl_start_display()
			game_summary = event["SUMMARY"]
			summary_split = game_summary.split()
			ScoreboardData.home_team = summary_split[2]
			ScoreboardData.away_team = summary_split[0]
			print(str(ScoreboardData.game_day) + " @ " + ScoreboardData.game_time + ": " + ScoreboardData.home_team + " vs " + ScoreboardData.away_team)

			ScoreboardData.nwhl_display_games()

def ritmhky_dump():
	for entry in ScoreboardData.ritmhky_data.entries:
		try:
			date = datetime.strptime(entry.s_localstartdate, '%Y-%m-%dT%H:%M:%S.%f0')
			ScoreboardData.game_day = date.strftime('%b %-d')
			ScoreboardData.game_time = date.strftime('%-I:%M%p')
		except ValueError:
			date = datetime.strptime(entry.s_localstartdate, '%Y-%m-%d')
			ScoreboardData.game_day = date.strftime('%b %-d')
			ScoreboardData.game_time = "TBD"
		if ScoreboardData.game_day == today:
			ScoreboardData.ncaamhcky_start_display()
			
			ScoreboardData.game_clock = ScoreboardData.game_day
			ScoreboardData.current_period = ScoreboardData.game_time
			ScoreboardData.game_score = ""

			if " at " in entry.title:
				ScoreboardData.home_team = entry.s_opponent
				ScoreboardData.away_team = "RIT"
			else:
				ScoreboardData.home_team = "RIT"
				ScoreboardData.away_team = entry.s_opponent
			
			description_break = entry.description.split('\\n')
			if "POSTPONED" in description_break[0]:
				ScoreboardData.status = "Postponed"
				ScoreboardData.game_clock = ""
				ScoreboardData.current_period = "POSTPONED"
				print(ScoreboardData.current_period)
			elif "CANCELED" in description_break[0]:
				ScoreboardData.status = "Canceled"
				ScoreboardData.game_clock = ""
				ScoreboardData.current_period = "CANCELED"

			elif "[" in description_break[0]:
				ScoreboardData.status = "Final"
				scores = description_break[1].split()
				score_split = scores[1].split("-")
				rit_score = int(score_split[0])
				opponent_score = int(score_split[1])
				if len(scores) > 2:
					if "Shootout" in scores[2]:
						ScoreboardData.game_clock = "F/SO"
						ScoreboardData.current_period = ""
						if "Win" in scores[3]:
							rit_score += 1
						else:
							opponent_score += 1
					elif "Overtime" in scores[2]:
						ScoreboardData.game_clock = "F/OT"
						ScoreboardData.current_period = ""
				else:
					ScoreboardData.game_clock = "FINAL"
					ScoreboardData.current_period = ""
				if ScoreboardData.home_team == "RIT":
					ScoreboardData.game_score = str(rit_score) + "-" + str(opponent_score)
				else:
					ScoreboardData.game_score = str(opponent_score) + "-" + str(rit_score)

			else:
				ScoreboardData.status = "Scheduled"
				#print("Game Upcoming")

			ScoreboardData.ritmhky_display_scores()
		
def ritwhky_dump():
	for entry in ScoreboardData.ritwhky_data.entries:
		try:
			date = datetime.strptime(entry.s_localstartdate, '%Y-%m-%dT%H:%M:%S.%f0')
			ScoreboardData.game_day = date.strftime('%b %-d')
			ScoreboardData.game_time = date.strftime('%-I:%M%p')
		except ValueError:
			date = datetime.strptime(entry.s_localstartdate, '%Y-%m-%d')
			ScoreboardData.game_day = date.strftime('%b %-d')
			ScoreboardData.game_time = "TBD"
		#print(ScoreboardData.game_day)
		if ScoreboardData.game_day == today:
			ScoreboardData.ncaawhcky_start_display()
			
			ScoreboardData.game_clock = ScoreboardData.game_day
			ScoreboardData.current_period = ScoreboardData.game_time
			ScoreboardData.game_score = ""

			if " at " in entry.title:
				ScoreboardData.home_team = entry.s_opponent
				ScoreboardData.away_team = "RIT"
			else:
				ScoreboardData.home_team = "RIT"
				ScoreboardData.away_team = entry.s_opponent

			#print(ScoreboardData.home_team + " vs " + ScoreboardData.away_team)
			description_break = entry.description.split('\\n')
			if "POSTPONED" in description_break[0]:
				ScoreboardData.status = "Postponed"
				ScoreboardData.game_clock = ""
				ScoreboardData.current_period = "POSTPONED"
				print(ScoreboardData.current_period)
			elif "CANCELED" in description_break[0]:
				ScoreboardData.status = "Canceled"
				ScoreboardData.game_clock = ""
				ScoreboardData.current_period = "CANCELED"

			elif "[" in description_break[0]:
				ScoreboardData.status = "Final"
				scores = description_break[1].split()
				score_split = scores[1].split("-")
				rit_score = int(score_split[0])
				opponent_score = int(score_split[1])
				if len(scores) > 2:
					if "Shootout" in scores[2]:
						ScoreboardData.game_clock = "F/SO"
						ScoreboardData.current_period = ""
						if "Win" in scores[3]:
							rit_score += 1
						else:
							opponent_score += 1
					elif "Overtime" in scores[2]:
						ScoreboardData.game_clock = "F/OT"
						ScoreboardData.current_period = ""
				else:
					ScoreboardData.game_clock = "FINAL"
					ScoreboardData.current_period = ""
				if ScoreboardData.home_team == "RIT":
					ScoreboardData.game_score = str(rit_score) + "-" + str(opponent_score)
				else:
					ScoreboardData.game_score = str(opponent_score) + "-" + str(rit_score)

			else:
				ScoreboardData.status = "Scheduled"
				#print("Game Upcoming")

			ScoreboardData.ritwhky_display_scores()
			
def nascar_dump():
	for event in ScoreboardData.nascar_data["series_3"]:
		current_date = datetime.strptime(event["race_date"], "%Y-%m-%dT%H:%M:%S")
		ScoreboardData.schedule_date = current_date.strftime("%b %-d")
		ScoreboardData.schedule_time = current_date.strftime("%H:%M:%S")
		#ScoreboardData.schedule_time = current_date.strftime("%-I:%M%p")
		if ScoreboardData.schedule_date == today:
			print("Truck Series Race Today")
			ScoreboardData.series_name = "Truck Series"
			ScoreboardData.track = event["track_name"]
			#ScoreboardData.track = ScoreboardData.track.strip(" ")
			ScoreboardData.race_time = datetime.strptime(event["race_date"], "%Y-%m-%dT%H:%M:%S").strftime("%-I:%M%p")
			ScoreboardData.series = "series_3"
			ScoreboardData.race_id = event["race_id"]
			
			ScoreboardData.nascar_start_display()
			ScoreboardData.nascar_display()
	for event in ScoreboardData.nascar_data["series_2"]:
		current_date = datetime.strptime(event["race_date"], "%Y-%m-%dT%H:%M:%S")
		ScoreboardData.schedule_date = current_date.strftime("%b %-d")
		ScoreboardData.schedule_time = current_date.strftime("%H:%M:%S")
		if ScoreboardData.schedule_date == today:
			print("Xfinity Series Race Today")
			ScoreboardData.series_name = "Xfinity Series"
			ScoreboardData.track = event["track_name"]
			#ScoreboardData.track = ScoreboardData.track.strip(" ")
			ScoreboardData.race_time = datetime.strptime(event["race_date"], "%Y-%m-%dT%H:%M:%S").strftime("%-I:%M%p")
			ScoreboardData.series = "series_2"
			ScoreboardData.race_id = event["race_id"]
			
			ScoreboardData.nascar_start_display()
			ScoreboardData.nascar_display()
	for event in ScoreboardData.nascar_data["series_1"]:
		current_date = datetime.strptime(event["race_date"], "%Y-%m-%dT%H:%M:%S")
		ScoreboardData.schedule_date = current_date.strftime("%b %-d")
		ScoreboardData.schedule_time = current_date.strftime("%H:%M:%S")
		if ScoreboardData.schedule_date == today:
			print("Cup Series Race Today")
			ScoreboardData.series_name = "Cup Series"
			ScoreboardData.track = event["track_name"]
			#ScoreboardData.track = ScoreboardData.track.strip(" ")
			ScoreboardData.race_time = datetime.strptime(event["race_date"], "%Y-%m-%dT%H:%M:%S").strftime("%-I:%M%p")
			ScoreboardData.series = "series_1"
			ScoreboardData.race_id = event["race_id"]
			
			ScoreboardData.nascar_start_display()
			ScoreboardData.nascar_display()
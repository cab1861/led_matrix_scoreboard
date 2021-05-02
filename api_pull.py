import requests
import json
import icalendar
import feedparser

from datetime import datetime
from icalendar import Calendar
from render import ScoreboardData
today = datetime.today()

def nhl_preferred_request():
	# NHL API Call
	print("Pulling Sabres Game Data")
	nhl_preferred = requests.get(ScoreboardData.nhl_root_location + "schedule?teamId=7&hydrate=linescore")
	ScoreboardData.nhl_preferred_data = nhl_preferred.json()
	
def nhl_request():
	# NHL API Call
	print("Pulling NHL API Data")
	nhl = requests.get(ScoreboardData.nhl_root_location + "schedule?hydrate=linescore")
	ScoreboardData.nhl_data = nhl.json()

def nfl_request():
	# NFL API Call
	print("Pulling NFL API Data")
	nfl = requests.get("http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
	ScoreboardData.nfl_data = nfl.json()
	
def nwhl_request():
	# NWHL iCal Call
	print("Pulling NWHL Data")
	nwhl = requests.get("https://calendar.google.com/calendar/ical/f6ukfbsmpqei7uq6dr8orcpabr8vm53k%40import.calendar.google.com/public/basic.ics").text
	ScoreboardData.nwhl_data = icalendar.Calendar.from_ical(nwhl)
	
	# TO DO: SORT GAMES BY DATE
	
def ritmhky_request():
	# RIT Men's RSS
	print("Pulling RIT Men's Hockey Data")
	ScoreboardData.ritmhky_data = feedparser.parse("https://ritathletics.com/calendar.ashx/calendar.rss?sport_id=9")

def ritwhky_request():
	# RIT Women's iCal
	print("Pulling RIT Women's Hockey Data")
	try:
		ScoreboardData.ritwhky_data = feedparser.parse("https://ritathletics.com/calendar.ashx/calendar.rss?sport_id=10")
	except:
		print("Error")
	
def nascar_request():
	# NASCAR Cup Series API Call
	print("Pulling NASCAR Data")
	nascar = requests.get("https://cf.nascar.com/cacher/2021/race_list_basic.json")
	ScoreboardData.nascar_data = nascar.json()
from weatherapp import db
from models import Location, User
from xml.dom import minidom
from datetime import datetime
import requests
import json
import os

def eval_weather(weather, zipcode):
	"""
	Determine if the weather is good or bad.  If the weather is fine we don't send an alert.
	Weather codes are found in the wwoConditionCodes.xml
	"""
	#weather = json.loads(weather)
	ignore_codes=['248', '143', '122', '119', '116', '113']

	#Book Keeping in the DB
	date = datetime.now()
	entry = Location.query.filter(Location.zipcode == zipcode).update({'last_updated':date})

	if not weather['data']['weather'][0]['weatherCode'] in ignore_codes:
		description = get_description(weather['data']['weather'][0]['weatherCode'])
		#send_notication(description, weather)
		return description
	description = get_description(weather['data']['weather'][0]['weatherCode'])
	print description
	return description
	

def get_weather(zipcode):
	key = os.environ.get('WORLD_WEATHER_KEY')
	num_of_days='2'
	format='json'
	url = "http://free.worldweatheronline.com/feed/weather.ashx?q=%s&format=%s&num_of_days=%s&key=%s" % (zipcode, format, num_of_days, key)
	weather = requests.get(url).json()
	return eval_weather(weather, zipcode)


def get_description(code):
	doc = os.path.dirname(__file__)
	xmldoc = minidom.parse(doc + "/wwoConditionCodes.xml")
	itemlist = xmldoc.getElementsByTagName('condition')
	for item in itemlist:
		if item.getElementsByTagName('code')[0].firstChild.nodeValue == code:
			print item.getElementsByTagName('description')[0].firstChild.nodeValue
			return item.getElementsByTagName('description')[0].firstChild.nodeValue

def update_db():
	zipcodes = Location.query.all()
	for zipcode in zipcodes:
		get_weather(zipcode)




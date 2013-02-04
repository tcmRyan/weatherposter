from weatherapp import db
from models import Location, User
from xml.dom import minidom
from datetime import datetime, timedelta
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
	entry = Location.query.filter(Location.zipcode == zipcode).first()
	dateString = weather['data']['weather'][0]['date']
	date = datetime.strptime(dateString, '%Y-%m-%d')
	if entry.last_updated:
		notify = (entry.last_updated - date) > timedelta(days = 1)
		notify = True
	else:
		notify = True


	#if not weather['data']['weather'][0]['weatherCode'] in ignore_codes and notify:
	if notify:
		description = get_description(weather['data']['weather'][0]['weatherCode'])
		return description
		entry.last_updated = date
		send_notification(description, zipcode)
	else:
		return 'Already Notified'
	

def get_weather(zipcode):
	key = os.environ.get('WORLD_WEATHER_KEY')
	num_of_days='2'
	format='json'
	payload = {'q': zipcode, 'format': format, 'num_of_days': num_of_days, 'key': key}
	url = "http://free.worldweatheronline.com/feed/weather.ashx"
	weather = requests.get(url, params=payload).content
	weather = json.loads(weather)
	return weather
	eval_weather(weather, zipcode)


def get_description(code):
	doc = os.path.dirname(__file__)
	xmldoc = minidom.parse(doc + "/wwoConditionCodes.xml")
	itemlist = xmldoc.getElementsByTagName('condition')
	for item in itemlist:
		if item.getElementsByTagName('code')[0].firstChild.nodeValue == code:
			print item.getElementsByTagName('description')[0].firstChild.nodeValue
			return item.getElementsByTagName('description')[0].firstChild.nodeValue

def update_db():
	locations = Location.query.all()
	for location in locations:
		foo = get_weather(location.zipcode)
		return foo


def send_notification(description, zipcode):
    url = '/weatherposter'
    template = description
    notify_list = User.query.filter(User.zipcode == zipcode)
    return notify_list
    for user in notify_list:
    	access_token = user.access_token
        payload = {'access_token': access_token, 'href': url, 'template': template}
        url = "https://graph.facebook.com/%s/notifications" % user.facebook_id
        r = requests.post(url, params=payload)
    return 'Notifications Sent'


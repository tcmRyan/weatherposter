from weatherapp import db
from models import Location, FBUser
from xml.dom import minidom
from datetime import datetime, timedelta
import requests
import json
import os
import fb_lib

def eval_weather(weather, zipcode):
	"""
	Determine if the weather is good or bad.  If the weather is fine we don't send an alert.
	Weather codes are found in the wwoConditionCodes.xml
	"""
	ignore_codes=['248', '143', '122', '119', '116', '113']

	#Book Keeping in the DB
	entry = Location.query.filter(Location.zipcode == zipcode).first()
	dateString = weather['data']['weather'][0]['date']
	date = datetime.strptime(dateString, '%Y-%m-%d')
	if entry.last_updated:
		notify = (entry.last_updated - date) > timedelta(days = 1)
	else:
		entry.last_updated = date
		db.session.commit()
		notify = True

	code = weather['data']['weather'][0]['weatherCode']
	description = get_description(code)

	if not (code in ignore_codes) and notify:
		entry.last_updated = date
		db.session.commit()
		test = send_notification(description, zipcode)
		return test
	else:
		if not code in ignore_codes:
			return 'Good Weather: %s' %  description
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
	test = eval_weather(weather, zipcode)
	return test

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
    notify_list = FBUser.query.filter(FBUser.zipcode == zipcode)
    FB_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    access_token = fb_lib.fbapi_get_application_access_token(FB_APP_ID)
    for user in notify_list:
        payload = {'access_token': access_token, 'href': url, 'template': template}
        url = "https://graph.facebook.com/%s/notifications" % user.facebook_id
        r = requests.post(url, params=payload)
    return r.content


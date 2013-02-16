from weatherapp import db
from datetime import datetime

class FBUser(db.Model):
	facebook_id = db.Column(db.String(120), primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(120), unique=True)
	zipcode = db.Column(db.String(5))
	access_token = db.Column(db.String(256))

	def __init__(self, facebook_id, name, email, zipcode, access_token):
		self.facebook_id = facebook_id
		self.name = name
		self.email = email
		self.zipcode = zipcode
		self.access_token = access_token

	def __repr__(self):
		return '<Name %r>' % self.name

class Location(db.Model):
	zipcode = db.Column(db.String(5), primary_key=True)
	last_updated = db.Column(db.DateTime)


	def __init__(self, zipcode, last_updated):
		self.zipcode = zipcode
		self.last_updated = last_updated

	def __repr__(self):
		return '<zipcode %r>' % self.zipcode

from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(120), unique=True)
	zipcode = db.Column(db.Integer)

	def __init__(self, name, email, zipcode):
		self.name = name
		self.email = email
		self.zipcode = zipcode

	def __repr__(self):
		return '<Name %r>' % self.name

class Location(db.Model):
	zipcode = db.Column(db.Integer, primary_key=True)
	last_updated = db.Column(db.DateTime)

	def __init__(self, zipcode, last_updated):
		self.zipcode = zipcode
		self.last_updated = last_updated

	def __repr__(self):
		return '<zipcode %r>' % self.zipcode

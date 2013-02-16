#!/usr/bin/env python

import requests

def update_db():
	requests.post('http://weatherposter.herokuapp.com/weathertest/')

if __name__ == '__main__':
	update_db()
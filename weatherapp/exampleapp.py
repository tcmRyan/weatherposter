# -*- coding: utf-8 -*-

import requests
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, redirect, render_template, url_for

from weatherapp import app, db
from models import User, Location
import weather
import fb_lib
import os

FB_APP_ID = os.environ.get('FACEBOOK_APP_ID')
requests = requests.session()

app_url = 'https://graph.facebook.com/{0}'.format(FB_APP_ID)
FB_APP_NAME = json.loads(requests.get(app_url).content).get('name')
FB_APP_SECRET = os.environ.get('FACEBOOK_SECRET')


@app.route('/', methods=['GET', 'POST'])
def index():
    # print get_home()

    access_token = fb_lib.get_token()
    channel_url = url_for('get_channel', _external=True)
    channel_url = channel_url.replace('http:', '').replace('https:', '')

    if access_token:

        me = fb_lib.fb_call('me', args={'access_token': access_token})
        if User.query.filter(User.facebook_id == me['id']).count() == 0:
            create_user(me, access_token)
        elif User.query.filter(User.facebook_id == me['id']).first():
            user = User.query.filter(User.facebook_id == me['id']).first()
            user.access_token = access_token[0]
            db.session.commit()
        fb_app = fb_lib.fb_call(FB_APP_ID, args={'access_token': access_token})
        likes = fb_lib.fb_call('me/likes',
                        args={'access_token': access_token, 'limit': 4})
        friends = fb_lib.fb_call('me/friends',
                          args={'access_token': access_token, 'limit': 4})
        photos = fb_lib.fb_call('me/photos',
                         args={'access_token': access_token, 'limit': 16})

        redir = fb_lib.get_home() + 'close/'
        POST_TO_WALL = ("https://www.facebook.com/dialog/feed?redirect_uri=%s&"
                        "display=popup&app_id=%s" % (redir, FB_APP_ID))

        app_friends = fb_lib.fql(
            "SELECT uid, name, is_app_user, pic_square "
            "FROM user "
            "WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) AND "
            "  is_app_user = 1", access_token)

        SEND_TO = ('https://www.facebook.com/dialog/send?'
                   'redirect_uri=%s&display=popup&app_id=%s&link=%s'
                   % (redir, FB_APP_ID, get_home()))

        url = request.url

        return render_template(
            'index.html', app_id=FB_APP_ID, token=access_token, likes=likes,
            friends=friends, photos=photos, app_friends=app_friends, app=fb_app,
            me=me, POST_TO_WALL=POST_TO_WALL, SEND_TO=SEND_TO, url=url,
            channel_url=channel_url, name=FB_APP_NAME)
    else:
        return render_template('login.html', app_id=FB_APP_ID, token=access_token, url=request.url, channel_url=channel_url, name=FB_APP_NAME)

@app.route('/channel.html', methods=['GET', 'POST'])
def get_channel():
    return render_template('channel.html')


@app.route('/close/', methods=['GET', 'POST'])
def close():
    return render_template('close.html')

@app.route('/dbtest/', methods=['GET', 'POST'])
def dbtest():
    if request.method =='GET':
        return render_template('dbtest.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        zipcode = request.form.get('zipcode')
        user = User(name, email, zipcode)
        db.session.add(user)
        db.session.commit()
        all_users = User.query.all()
        if Location.query.filter(Location.zipcode == zipcode).count() == 0:
            date = datetime.now()
            new_location = Location(zipcode, date)
            db.session.add(new_location)
            db.session.commit()
        all_zipcodes = Location.query.all()
        return render_template('results.html', users=all_users, locations=all_zipcodes)

def create_user(user_dict, access_token):
    facebook_id = user_dict['id']
    name = user_dict['name']
    email = user_dict['email']
    zipcode = None
    user = User(facebook_id, name, email, zipcode, access_token[0])
    db.session.add(user)
    db.session.commit()

@app.route('/update-user/', methods=['GET', 'POST'])
def update_user():
    token = fb_lib.get_token()
    zipcode = request.form['zipcode']
    me = fb_lib.fb_call('me', args={'access_token': token})
    record =  User.query.filter(User.facebook_id == me['id']).first()
    record.zipcode = zipcode
    db.session.commit()
    if Location.query.filter(Location.zipcode == zipcode).count() == 0:
        date = None
        new_location = Location(request.form['zipcode'], date)
        db.session.add(new_location)
        db.session.commit()
    return render_template('results.html')

@app.route('/weathertest/', methods=['POST'])
def weathertest():
    if request.method == 'POST':
        result = weather.update_db()
        return render_template('test.html', description=result)



from weatherapp import app
import os
FBAPI_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FBAPI_APP_SECRET = os.environ.get('FACEBOOK_SECRET')
port = int(os.environ.get("PORT", 5000))
if FBAPI_APP_ID and FBAPI_APP_SECRET:
	app.run(host='0.0.0.0', port=port)
else:
    print 'Cannot start application without Facebook App Id and Secret set'
from weatherapp import app
import os

port = int(os.environ.get("PORT", 5000))
if app.config.get('FB_APP_ID') and app.config.get('FB_APP_SECRET'):
	app.run(host='0.0.0.0', port=port)
else:
    print 'Cannot start application without Facebook App Id and Secret set'
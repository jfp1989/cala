import functools
import json
import os
import flask

from authlib.client import OAuth2Session

import google_auth

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(google_auth.app)

@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        if user_info['email'] == "ezequiel.uhrig@gmail":
            return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"
        else:
            return "Not authorized"
    return 'You are not currently logged in.'
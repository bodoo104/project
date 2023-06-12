from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os


app = Flask(__name__)
app.secret_key = os.urandom(12)

oauth = OAuth(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/google/')
def google():

    GOOGLE_CLIENT_ID = '458345810569-o4i4724hb0viap86q2m37qcu6c268a9k.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print(" Google User ", user)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

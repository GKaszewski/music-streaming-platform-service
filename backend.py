from flask import Flask, Response, render_template, Markup, jsonify
import markdown, os
import firebase_admin as fb
from firebase_admin import db, auth
from api import Song

app = Flask(__name__)

#Firebase database configuration
credsPath = os.path.join(app.root_path, 'creds.json')
creds = fb.credentials.Certificate(credsPath)
firebaseApp = fb.initialize_app(creds, {
    "databaseURL": 'https://musicstreamingplatform.firebaseio.com/'
})
##


@app.route("/")
def index():
    with open("readme.md", 'r') as markdown_file:
        content = markdown_file.read()
        page = Markup(markdown.markdown(content))
        return page

@app.route("/song/<title>")
def getSong(title):
    songObj = fb.db.reference('/{}'.format(title)).child('0')
    songRef = Song.create(songObj)
    return jsonify(albumName = songRef.albumName, albumUrl = songRef.albumUrl, author = songRef.author, songUrl = songRef.songUrl, tags = songRef.tags, title = songRef.title)  

@app.route("/song/search/<query>")
def getSongsByQuery(query):
    return 'nothing here yet...'

@app.route('/auth/create/user/<email>&<password>')
def postNewUser(email, password):
    fb.auth.create_user({'email': emial, 'password': password})

@app.route('/auth/login/user/<email>&password')
def loginUser(email, password):
    fb.auth.get_user_by_email(email)

#bbb
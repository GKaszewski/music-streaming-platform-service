from flask import Flask, Response, render_template, Markup, jsonify
import markdown, os, collections, json
import firebase_admin as fb
from firebase_admin import db
from api import Song

app = Flask(__name__)

#Firebase database configuration
credsPath = os.path.join(app.root_path, 'creds.json')
creds = fb.credentials.Certificate(credsPath)
firebaseApp = fb.initialize_app(creds, {
    "databaseURL": 'https://musicstreamingplatform.firebaseio.com/'
})
db = fb.db.reference('/')
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
    songs = db.order_by_key().start_at(query).end_at(u'{0}\uf8ff'.format(query)).get()
    listOfSongs = []
    for key, val in songs.items():
        songRef = Song.createFromDict(val[0])
        listOfSongs.append(json.loads(songRef.toJson()))

    return jsonify(listOfSongs)

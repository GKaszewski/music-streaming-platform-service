from flask import Flask, Response, render_template, Markup, jsonify, flash, redirect
import markdown, os, collections, json, forms
import firebase_admin as fb
from firebase_admin import db
from api import Song
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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
        return render_template('index.html', title='Music Streaming Platform Service', content=page)

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

@app.route('/upload/song', methods=['GET', 'POST'])
def uploadSong():
    tags = ['']
    uploadingForm = forms.SongForm()
    if uploadingForm.validate_on_submit():
        newSongNode = db.update({
        '{}/0/albumName'.format(uploadingForm.songName.data.lower()) : uploadingForm.albumName.data, 
        '{}/0/albumUrl'.format(uploadingForm.songName.data.lower()): uploadingForm.cover.data,
        '{}/0/author'.format(uploadingForm.songName.data.lower()): uploadingForm.author.data,
        '{}/0/songUrl'.format(uploadingForm.songName.data.lower()): uploadingForm.songUrl.data,
        '{}/0/title'.format(uploadingForm.songName.data.lower()): uploadingForm.songName.data,
        '{}/0/tags'.format(uploadingForm.songName.data.lower()): tags})
        flash('Uploading {}'.format(uploadingForm.songName.data))
        return redirect('/')

    return render_template('songForm.html', title='Upload song', form=uploadingForm)

app.run(debug=True)
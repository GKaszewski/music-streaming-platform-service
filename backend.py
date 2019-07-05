from flask import Flask, Response, render_template, Markup, jsonify, flash, redirect
import markdown
import os
import collections
import json
import forms
import firebase_admin as fb
from firebase_admin import db, firestore
from api import Song
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Firebase database configuration
credsPath = os.path.join(app.root_path, 'creds.json')
creds = fb.credentials.Certificate(credsPath)
firebaseApp = fb.initialize_app(creds, {
    "databaseURL": 'https://musicstreamingplatform.firebaseio.com/'
})
db = fb.db.reference('/')
userDB = firestore.client()
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
    return jsonify(albumName=songRef.albumName, albumUrl=songRef.albumUrl, author=songRef.author, songUrl=songRef.songUrl, tags=songRef.tags, title=songRef.title)


@app.route("/song/search/<query>")
def getSongsByQuery(query):
    songs = db.order_by_key().start_at(query).end_at(
        u'{0}\uf8ff'.format(query)).get()
    listOfSongs = []
    for key, val in songs.items():
        songRef = Song.createFromDict(val[0])
        listOfSongs.append(json.loads(songRef.toJson()))

    return jsonify(listOfSongs)


doc = userDB.collection(u'users')


@app.route('/playlist/create/<user>&<playlistName>')
def createPlaylist(user, playlistName):
    newUser = doc.document(u'{}'.format(user))
    newUser.set({
        u'playlists': {
            '{}'.format(playlistName) : {
               
            },
        }
    }, merge=True)
    return 'it works'

@app.route('/playlist/<user>&<name>/add_song/<albumName>&<path:cover>&<title>&<path:songUrl>&<author>')
def addSongToPlaylist(user, name, albumName, title, songUrl, cover, author):
    playlists = doc.document(u'{}'.format(user)).get().to_dict()['playlists']
    playlist = playlists[name]
    song = Song.createFromDict({
        'albumName' : albumName,
        'albumUrl' : cover,
        'author' : author,
        'songUrl' : songUrl,
        'title' : title,
        'tags' : [''],
    })
    playlist.update(song.to_dict())
    doc.document(u'{}'.format(user)).update({
        u'playlists': {
            u'{}'.format(name) : playlist 
        }
    })
    
    return jsonify(albumName=song.albumName, cover=song.albumUrl, title=song.title, songUrl=song.songUrl, author=song.author)

@app.route('/upload/song', methods=['GET', 'POST'])
def uploadSong():
    tags = ['']
    uploadingForm = forms.SongForm()
    if uploadingForm.validate_on_submit():
        newSongNode = db.update({
            '{}/0/albumName'.format(uploadingForm.songName.data.lower()): uploadingForm.albumName.data,
            '{}/0/albumUrl'.format(uploadingForm.songName.data.lower()): uploadingForm.cover.data,
            '{}/0/author'.format(uploadingForm.songName.data.lower()): uploadingForm.author.data,
            '{}/0/songUrl'.format(uploadingForm.songName.data.lower()): uploadingForm.songUrl.data,
            '{}/0/title'.format(uploadingForm.songName.data.lower()): uploadingForm.songName.data,
            '{}/0/tags'.format(uploadingForm.songName.data.lower()): tags})
        flash('Uploading {}'.format(uploadingForm.songName.data))
        return redirect('/')

    return render_template('songForm.html', title='Upload song', form=uploadingForm)

app.route('/user/create/<userName>&<followers>&<following>')
def createUser(userName, followers, following):
    newUser = doc.document(u'{}'.format(userName))
    newUser.set({
        u'followers' : followers,
        u'following' : following,
        u'playlists' : {},
    })
    return 'done!'


app.run(debug=True)

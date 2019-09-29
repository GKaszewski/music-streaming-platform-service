# Music Streaming Platform service 

Songs
======

**Example song object**
```json
"bastille good grief": 
[
    {
    "albumName": "Wild world",
    "albumUrl":"https://firebasestorage.googleapis.com/v0/b/musicstreamingplatfor.appspot.com/o/Album%20covers%2Fwild%20world%20cover.jpegalt=media&token=fe3e5aca-5fa9-41dc-b917-31c4ccc1b678",
    "author": "Bastille",
    "songUrl":"https://firebasestorage.googleapis.com/v0/b/musicstreamingplatfor.appspot.com/o/Music%2F01.%20Good%20Grief.opus?alt=mediatoken=3a8cb9dd-7b8d-472d-b6e8-66c7821135d8",
    "tags": [
        "indie",
        "alternative"
    ],
    "title": "Good grief"
    }
],
```

# Different requests to get song or songs.

# Get song by title
**Definition**
`GET api/song/?search=title`

**Example Response**
* `200 OK` on success
```json
{
    "albumName": "Wild world",
    "albumUrl": "https://firebasestorage.googleapis.com/v0/b/musicstreamingplatform.appspot.com/o/Album%20covers%2Fwild%20world%20cover.jpeg?fea-5fa9-41dc-b917-31c4ccc1b678",
    "author": "Bastille",
    "songUrl": "https://firebasestorage.googleapis.com/v0/b/mus821135d8",
    "tags": [
        "indie",
        "alternative",
    ],
    "title": "Good grief"
}
```

# Get song/s by search query
**Definition**
`GET api/song/?search=query`

**Example Response**
* `200 OK` on success
```json
[
    "bastille good grief": 
    [
        {
        "albumName": "Wild world",
        "albumUrl": "https://firebasestorage.googleapis.com/v0/b/musicstreamingplatform.appspot.com/o/Album%20covers%2Fwild%20world%20cover.jpeg?alt=media&token=fe3e5aca-5fa9-41dc-b917-31c4ccc1b678",
        "author": "Bastille",
        "songUrl": "https://firebasestorage.googleapis.com/v0/b/musicstreamingplatform.appspot.com/o/Music%2F01.%20Good%20Grief.opus?alt=media&token=3a8cb9dd-7b8d-472d-b6e8-66c7821135d8",
        "tags": [
            "indie",
            "alternative"
        ],
        "title": "Good grief"
        }
    ],
    "bastille good grief": 
    [
        {
        "albumName": "Wild world",
        "albumUrl": "https://firebasestorage.googleapis.com/v0/b/musicstreamingplatform.appspot.com/o/Album%20covers%2Fwild%20world%20cover.jpeg?alt=media&token=fe3e5aca-5fa9-41dc-b917-31c4ccc1b678",
        "author": "Bastille",
        "songUrl": "https://firebasestorage.googleapis.com/v0/b/musicstreamingplatform.appspot.com/o/Music%2F01.%20Good%20Grief.opus?alt=media&token=3a8cb9dd-7b8d-472d-b6e8-66c7821135d8",
        "tags": [
            "indie",
            "alternative"
        ],
        "title": "Good grief"
        }
    ],
]
```

Playlists
=========
## Create playlist
**Definition**
`POST api/playlist/create/<user>&<playlistName>`

## Add song to the playlist
**Definition**
`POST api/playlist/<user>&<playlistName>/add_song/<albumName>&<cover>&<title>&<songUrl>&<author>`

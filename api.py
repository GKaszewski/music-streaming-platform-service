import json

class Song:
    albumName = ""
    albumUrl = ""
    author = ""
    songUrl = ""
    tags = []
    title = ""

    def __init__(self, albumName, albumUrl, author, songUrl, tags, title):
        self.title = title
        self.tags = tags
        self.songUrl = songUrl
        self.author = author
        self.albumUrl = albumUrl
        self.albumName = albumName

    def create(songObj):
        newSong = Song(songObj.child('albumName').get(), songObj.child('albumUrl').get(), songObj.child('author').get(), songObj.child('songUrl').get(), songObj.child('tags').get(), songObj.child('title').get())
        return newSong

    def createFromDict(dict):
        newSong = Song(dict['albumName'], dict['albumUrl'], dict['author'], dict['songUrl'], dict['tags'], dict['title'])
        return newSong

    def getSongUrl(self):
        return self.songUrl

    def getAlbumUrl(self):
        return self.albumUrl

    def toJson(self):
        obj = {
            'albumName':self.albumName,
            'albumUrl':self.albumUrl,
            'author':self.author,
            'songUrl':self.songUrl,
            'tags':self.tags,
            'title':self.title,
        }

        return json.dumps(obj)


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

    def getSongUrl(self):
        return self.songUrl

    def getAlbumUrl(self):
        return self.albumUrl


class User:
    email = "";
    password = "";

    def __init__(self, email, password):
        self.email = email;
        self.password = password;


#bb
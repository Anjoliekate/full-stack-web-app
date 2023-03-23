import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class SongsDB:

    def __init__(self):
        self.connection = sqlite3.connect("songs_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def createSongs(self, name, album, genre, artist, year):
        # do not concactinate when inserting, make sure to store data and query it seperately to avoid sql injection
        data = [name, album, genre, artist, year]
        self.cursor.execute(
            "INSERT INTO songs(name, album, genre, artist, year) VALUES (?, ?, ?, ?, ?)", data)
        self.connection.commit()

    def getAllSongs(self):
        self.cursor.execute("SELECT * FROM songs")
        records = self.cursor.fetchall()
        return records

    # returns a single dictionary (or None if the song_id does not exist)
    def getOneSong(self, song_id):
        data = [song_id]
        self.cursor.execute("SELECT * FROM songs WHERE id = ?", data)
        record = self.cursor.fetchone()
        return record

    def deleteSong(self, song_id):
        data = [song_id]
        self.cursor.execute("DELETE FROM songs WHERE id = ?", data)
        self.connection.commit()

    def updateSong(self, song_id, name, album, genre, artist, year):
        data = [name, album, genre, artist, year, song_id]
        self.cursor.execute(
            "UPDATE songs SET name = ?, album = ?, genre = ?, artist = ?, year = ? WHERE id = ?", data)
        self.connection.commit()

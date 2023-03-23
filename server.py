
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from socketserver import ThreadingMixIn
from songs_db import SongsDB


class MyRequestHandler(BaseHTTPRequestHandler):

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))

    def handleGetSongsCollection(self):
        db = SongsDB()
        allSongs = db.getAllSongs()
        # response status code first then headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        # response body ->

        # UTF-8 is compatible with ascii
        self.wfile.write(bytes(json.dumps(allSongs), "utf-8"))

    def handleGetSongsMember(self, song_id):
        db = SongsDB()
        oneSong = db.getOneSong(song_id)

        if oneSong != None:
            # response status code:
            self.send_response(200)
            # response header:
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # response body:
            self.wfile.write(bytes(json.dumps(oneSong), "utf-8"))  # jsonify
        else:
            self.handleNotFound()

    def handleDeleteSong(self, member_id):
        db = SongsDB()
        member = db.getOneSong(member_id)
        # 1. read the date in the request body
        if member:
            try:
                db.deleteSong(member_id)

                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()  # always end headers even if you don't send any

            except:
                self.send_response(500)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def handleUpdateSong(self, member_id):
        db = SongsDB()
        member = db.getOneSong(member_id)
        # 1. read the date in the request body
        if member:
            try:
                length = int(self.headers["Content-Length"])
                request_body = self.rfile.read(length).decode("utf-8")
                parsed_body = parse_qs(request_body)

                name = parsed_body["name"][0]
                album = parsed_body["album"][0]
                genre = parsed_body["genre"][0]
                artist = parsed_body["artist"][0]
                year = parsed_body["year"][0]

                db.updateSong(member_id, name, album, genre, artist, year)

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()  # always end headers even if you don't send any

            except:
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()  # always end headers even if you don't send any

    def handleCreateSong(self):
        print("request headers:", self.headers)

        # 1. read the date in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body: ", parsed_body)

        # 2. append to MY_SONGS
        name = parsed_body["name"][0]
        album = parsed_body["album"][0]
        genre = parsed_body["genre"][0]
        artist = parsed_body["artist"][0]
        year = parsed_body["year"][0]

        db = SongsDB()
        db.createSongs(name, album, genre, artist, year)

        # 3. send a response
        self.send_response(201)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()  # always end headers even if you don't send any

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            member_id = None

        if collection_name == "songs":
            if member_id:
                self.handleGetSongsMember(member_id)
            else:
                self.handleGetSongsCollection()
        else:
            self.handleNotFound()

    def do_POST(self):
        if self.path == "/songs":
            self.handleCreateSong()
        else:
            self.handleNotFound()

    def do_DELETE(self):
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        if collection_name == "songs":
            self.handleDeleteSong(member_id)
        else:
            self.handleNotFound()

    def do_PUT(self):
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        if collection_name == "songs":
            self.handleUpdateSong(member_id)
        else:
            self.handleNotFound()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer(listen, MyRequestHandler)

    print("Server running!")
    server.serve_forever()


if __name__ == '__main__':
    run()

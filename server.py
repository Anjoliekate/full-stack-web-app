from session_store import SessionStore
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from socketserver import ThreadingMixIn
from songs_db import SongsDB
from http import cookies
from passlib.hash import bcrypt

SESSION_STORE = SessionStore()


class MyRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        super().end_headers()

    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

        print(self.headers["Cookie"])

    def loadSession(self):
        # load the cookie data and check for existance of the session ID cookie
        self.loadCookie()
        if 'sessionId' in self.cookie:
            # load the session data for the sessionID
            sessionId = self.cookie['sessionId'].value
            self.sessionData = SESSION_STORE.getSessionData(sessionId)
            if self.sessionData == None:
                # create a new session / session ID
                sessionId = SESSION_STORE.createSession()
                self.sessionData = SESSION_STORE.getSessionData(sessionId)
                # save the new session ID into a cookie
                self.cookie['sessionId'] = sessionId
                # load the session with the new session ID

            else:
                # create a new session / session ID
                sessionId = SESSION_STORE.createSession()
                self.sessionData = SESSION_STORE.getSessionData(sessionId)
                # save the new session ID into a cookie
                self.cookie['sessionId'] = sessionId
                # load the session with the new session ID

    def sendCookie(self):
        for morsel in self.cookie.values():
            if "Postman" not in self.header["User-Agent"]:
                morsel["samesite"] = "None"
                morsel["secure"] = True
            self.send_headers("Set-Cookie", morsel.OutputString())

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))

    def handle401(self):
        self.send_response(401)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not Authenticated.", "utf-8"))

    def handleGetSongsCollection(self):
        if "userId" not in self.sessionData():
            self.handle401()
            return

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
        else:
            self.send_response(404)
            self.end_headers()

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

    def handleCreateSession(self):
        print("request headers:", self.headers)

        # 1. read the date in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body: ", parsed_body)

        # 2. append to MY_Users
        email = parsed_body["email"][0]
        password = parsed_body['password'][0]

        db = SongsDB()
        user = db.checkUser(email)
        if user:
            if db.checkPassword(email, password):
                self.send_response(201)

                self.sessionData["userId"] = user["id"]
                self.end_headers()

            else:
                self.handle401()

        else:
            self.handle401()

    def handleCreateUser(self):
        # 1. read the date in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body: ", parsed_body)
        # 2. append to MY_Users
        firstName = parsed_body["firstName"][0]
        lastName = parsed_body["lastName"][0]
        email = parsed_body["email"][0]
        password = parsed_body["password"][0]

        db = SongsDB()
        exists = db.checkUser(email)

        if not exists:
            db.createUser(firstName, lastName, email, password)
            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(422)
            self.end_headers()

    def loginCheckUser(self):
        # 1. read the date in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body: ", parsed_body)
        # 2. append to MY_Users
        email = parsed_body["email"][0]
        password = parsed_body["password"][0]
        db = SongsDB()
        user = db.checkUser(email)
        if user:
            if db.checkPassword(email, password):
                self.loadSession()
                self.send_response(201)
                self.end_headers()
                self.sessionData = SESSION_STORE.getSessionData("userId")
                self.sessionData["userId"] = user["id"]

            else:
                self.handle401()

        else:
            self.handle401()

    def do_OPTIONS(self):
        self.loadSession()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.loadSession()
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
        self.loadSession()
        print("path is:", self.path)
        if self.path == "/songs":
            self.handleCreateSong()
            self.end_headers()
        elif self.path == "/users":
            self.handleCreateUser()
            self.end_headers()
        elif self.path == "/sessions":
            self.handleCreateSession()
            self.end_headers()
        else:
            self.handleNotFound()

    def do_DELETE(self):
        self.loadSession()
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        if collection_name == "songs":
            self.handleDeleteSong(member_id)
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.loadSession()
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

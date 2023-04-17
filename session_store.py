import os
import base64


class SessionStore:

    def __init__(self):
        # a dictionary of dictionaries, one for each session
        self.sessions = {}

    def createSession(self):
        # create new session dictionary, add to self.sessions
        # assign new seesion to new session ID
        sessionId = self.generateSessionId()
        self.sessions[sessionId] = {}
        return sessionId

    def generateSessionId(self):
        # return new session ID that is:
        #random, unique, unguessable
        id = os.urandom(32)
        rstr = base64.b64encode(id).decode("utf-8")
        return rstr

    def getSessionData(self, sessionID):
        # return the dictionary associated with the session ID, if it exists
        if sessionID in self.sessions:
            return self.sessions[sessionID]
        else:
            return None

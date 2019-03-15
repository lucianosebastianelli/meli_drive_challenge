from __future__ import print_function
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class auth:
    def __init__(self,SCOPES,CLIENT_CREDENTIALS_FILE, TOKEN_PICKLE_FILE):
        self.SCOPES = SCOPES
        self.CLIENT_CREDENTIALS_FILE = CLIENT_CREDENTIALS_FILE
        self.TOKEN_PICKLE_FILE = TOKEN_PICKLE_FILE

    def getCredentials(self):

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        TOKEN_PICKLE_FILE = self.TOKEN_PICKLE_FILE

        if os.path.exists(TOKEN_PICKLE_FILE):
            with open(TOKEN_PICKLE_FILE, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(TOKEN_PICKLE_FILE, 'wb') as token:
                pickle.dump(creds, token)
        return creds
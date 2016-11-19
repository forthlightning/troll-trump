from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import tweepy

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Troll-Trump-Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def update_status(api, new_status):
    api.update_status(status=new_status)

def get_tweetlist():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1e1p_5v-6YAGViz4rGjrGuJAs25f-AI8Spe6uyiWVhxY'
    rangeName = 'Response Repository!E2:E500'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])


    list_of_tweets = []

    if not values:
        print('No data found.')
    else:
        for row in values:
            try:
                list_of_tweets.append(row[0])
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s' % (row[0]))
            except IndexError:
                pass

    return list_of_tweets


def get_userIDlist():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1e1p_5v-6YAGViz4rGjrGuJAs25f-AI8Spe6uyiWVhxY'
    rangeName = "Influential Denier Twitter Handles!B2:B500"

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    userIDlist = []

    if not values:
        print('No data found.')
    else:
        for row in values:
            try:
                userIDlist.append(row[0])
            except IndexError:
                pass

    return userIDlist


def get_col_values(tab_name, col):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1e1p_5v-6YAGViz4rGjrGuJAs25f-AI8Spe6uyiWVhxY'
    rangeName = tab_name+"!"+col+"2:"+col+"500"

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    userIDlist = []

    if not values:
        print('No data found.')
    else:
        for row in values:
            try:
                userIDlist.append(row[0])
            except IndexError:
                pass

    return userIDlist

def login_user(consumer_key,consumer_secret,access_token,access_token_secret):
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api





credentials = {"chinahoax": {
        "consumer_key":"qGukKFrGvJkbbvAdaoJovhW0d",
        "consumer_secret":"f3q1rdhDlr0dGAyxOmQosJWalkg0YwDNtn7QUQp0fqPxgBYmhv",
        "access_token":"2902869899-nGULNzeuoNQSmlE5fY7db2vEEUlmGIvjzYhkVXs",
        "access_token_secret":"2CTfaZrgWIw16YhhNJN34DQebjwamQlGyd0h3IwsK6dQZ"},
    "chinahoax1":{
        "consumer_key":"ektj3xDdIxcWsJzhKdG5n062N",
        "consumer_secret":"K4gbdPlSTfrQHRtGFGo4S8z5JXMUEWhawCS4zPElZFLwnPDtGy",
        "access_token":"800077289132130304-RFxDYnYCk1LNWkbOBTQ02vgVQoBNdDT",
        "access_token_secret":"vzWHx7ZvPxPeLOJe9DInqZPoFY42xRFpZyTYHqRaAt39K"},
    "rushmore":{
        "consumer_key":"8ilI5mRkw4eIWvklKlErdhFkg",
        "consumer_secret":"IiJH05LmwrCX1FMX5jk9AlJzUAUX1rrHiiGBeBPosXcgtrgU0N",
        "access_token":"800076261565435904-G4SfNQJpgAIvwRljf3EVN4p1kWe6bhW",
        "access_token_secret":"nDNyc8mCfax29udOvrEEoHCPI2tDiSwLvCYzMrBFFMrvt"},
}

rushmore = credentials['rushmore']

api = login_user(rushmore['consumer_key'],rushmore['consumer_secret'],rushmore['access_token'],rushmore['access_token_secret'])
print(api)
twitter_handles = get_col_values(tab_name="Influential Denier Twitter Handles",col="A")
responses = get_col_values(tab_name="Response Repository",col="E")
# update_status(api, )
update_status(api, twitter_handles[0] + " " + responses[1])





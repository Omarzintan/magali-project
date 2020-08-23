from __future__ import print_function
from flask import Flask, jsonify, request, render_template
from flask_assets import Bundle, Environment
import ezsheets


import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import discovery
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
secret_file = os.path.join( 'client_secret.json')


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1kX_YT4AB2TjMurYKjmkvKrSix0C51lIkaHXBVpbx8r0'
SAMPLE_RANGE_NAME = 'Sheet1!A2:C'

app = Flask(__name__)

js = Bundle('script.js', output='gen/main.js')

assets = Environment(app)

assets.register('main_js', js)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json()) # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message) # serialize and use JSON headers

@app.route('/test')
def test_page():
    # look inside `templates` and serve `home.html`
    return render_template('home.html')

'''
# Returns data from Spreadsheet as a JSON file to script.js using ezsheets
@app.route('/data')
def getData():
    results = {}
    # Get the Spreadsheet.
    ss = ezsheets.Spreadsheet('1kX_YT4AB2TjMurYKjmkvKrSix0C51lIkaHXBVpbx8r0')
    # Make sure the Spreadsheet is the most recent version
    ss.refresh()
    sheet = ss[0]
    rows = sheet.getRows()
    columns = sheet.getColumns()
    headings = rows[0]
    i = 0
    while (headings[i] != ''):
        column = columns[i]
        j = 1
        results[headings[i]] = []
        while (column[j] != ''):
            results[headings[i]].append(column[j])
            j+=1
        i+=1
    return jsonify(results)
'''

# Returns data from Spreadsheet as a JSON file to script.js using google service
@app.route('/data1')
def getData1():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return
    else:
        print('Name, Major:')
        #for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s, %s' % (row[0], row[4]))
        return jsonify(values)

@app.route('/data2')
def getData2():
    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    return jsonify(values)

if __name__ == '__main__':
    app.run()

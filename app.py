import os
from flask import Flask, jsonify, request, render_template
from flask_assets import Bundle, Environment
import json

import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from apiclient import discovery
from google.oauth2 import service_account


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

@app.route('/data')
def getData():
    # set sheet_name to argument
    sheet_name = request.args.get('category')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    secret_file_var = os.environ.get('GOOGLE_CREDS', 'var not found')
    secret_file = json.loads(secret_file_var)
   

    SPREADSHEET_ID = '1ymSnsFKZGCtjU6idXxoVtWARedas7xIFcF_WcRyvkL0'
    RANGE_NAME = sheet_name+'!A2:B150'

    credentials = service_account.Credentials.from_service_account_info(secret_file, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    sheet_values = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    links = sheet_values.get('values', [])
    return jsonify(links)

if __name__ == '__main__':
    app.run()

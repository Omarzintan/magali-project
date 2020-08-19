from flask import Flask, jsonify, request, render_template
from flask_assets import Bundle, Environment
import ezsheets

app = Flask(__name__)

js = Bundle('script.js', output='gen/main.js')

assets = Environment(app)

assets.register('main_js', js)

@app.route('/')
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


# Returns data from Spreadsheet as a JSON file to script.js
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

if __name__ == '__main__':
    app.run()

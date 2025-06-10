from flask import Flask, render_template, request, redirect
from modules.URLConverter import URLConverter
import random
import string
import os
import sqlite3

app = Flask(__name__)

log = []
url_map = {}

@app.route('/<short_url>')
def redirect_short_url(short_url):
    log.append(f'redirect_short_url: {short_url}')
    if short_url in url_map:
        url = url_map[short_url]
        return redirect(url, code=302)
    else:
        return 'Short URL not found', 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten')
def shorten():
    url = request.args.get('url', 'https://example.com')
    # random 6 character string
    ch = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(ch, k=6))
    url_map[short_url] = url
    return short_url



def create_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            short_url TEXT PRIMARY KEY,
            original_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_db_test():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_test_data():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('INSERT INTO test (name) VALUES (?)', ('test_name',))
    conn.commit()
    conn.close()

def read_test_data():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM test')
    data = c.fetchall()
    conn.close()
    return data

@app.route('/db-add-test')
def db_add_test():
    insert_test_data()
    return "Test data added to test.db"

@app.route('/db-read-test')
def db_read_test():
    data = read_test_data()
    return "<br>".join([f"id: {row[0]}, name: {row[1]}" for row in data])


@app.route('/env')
def env():

    return "".join(f"{key}={value}" for key, value in sorted(request.environ.items()))

@app.route('/env-2')
def env_2():
    test = os.environ.get('test', 'default_value')
    return f"test={test}"

@app.route('/env-3')
def env_3():
    return "".join(f"{key}={value}" for key, value in sorted(os.environ.items()))



@app.route('/ping')
def ping():
    log.append('ping')
    return 'pong2'

@app.route('/log')
def get_log():
    return log





@app.route('/redirect')
def redirect_to_index():
    url = request.args.get('url', 'https://example.com')
    code = request.args.get('code', 302)
    mode = request.args.get('mode', 'plain')
    shift = request.args.get('shift', 13)

    if ('code' in request.args and request.args['code'].isdigit() and
        int(request.args['code']) in [301, 302, 303, 307, 308]):
        code = int(request.args['code'])
    else:
        code = 302

    converter = URLConverter(url, mode, shift)
    url = converter.convert()

    return redirect(url, code=code)



if __name__ == '__main__':
    create_db()
    create_db_test()
    app.run(host='0.0.0.0', port=5000, debug=True)
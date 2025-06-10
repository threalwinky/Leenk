from flask import *

app = Flask(__name__)

log = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    log.append('ping')
    return 'pong'

@app.route('/log')
def get_log():
    return log

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, redirect, send_from_directory
from modules.URLConverter import URLConverter
import random
import string
import os
import datetime
from modules.Webhook import Webhook
import time

app = Flask(__name__)

log = []
url_map = {}
webhook = Webhook()
URL = os.environ.get('URL', 'http://localhost:5000')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    log.append(f'redirect_short_url: short_url={short_url}, timestamp={datetime.datetime.now().isoformat()}')
    if short_url in url_map:
        url = url_map[short_url]
        return redirect(url, code=302)
    else:
        return render_template('error.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/url-shortener')
def url_shortener():
    return render_template('url-shortener.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'logo.jpg', mimetype='image/jpeg')

@app.route('/shorten', methods=['POST'])    
def shorten():
    url = request.form.get('url', 'https://example.com')
    ch = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(ch, k=6))
    url_map[short_url] = url
    log.append(f'shorten: url={url}, short_url={short_url}, timestamp={datetime.datetime.now().isoformat()}')
    return {"random_url" : URL + '/' + short_url}

@app.route('/custom_shorten', methods=['POST'])
def custom_shorten():
    url = request.form.get('url', 'https://example.com')
    custom_short_url = request.form.get('custom_short_url', '')
    if not custom_short_url or len(custom_short_url) < 2:
        return "Custom short URL must be at least 2 characters long", 400
    if custom_short_url in url_map:
        return "Custom short URL already exists", 400
    url_map[custom_short_url] = url
    log.append(f'custom_shorten: url={url}, custom_short_url={custom_short_url}, timestamp={datetime.datetime.now().isoformat()}')
    return {"custom_url" : URL + '/' + custom_short_url}

@app.route('/clear')
def clear_logs():
    password = os.environ.get('password', 'fake_password')
    input_password = request.args.get('password', '')
    log.append(f'clear_logs: timestamp={datetime.datetime.now().isoformat()}')
    if input_password != password:
        return "Unauthorized", 401
    log.clear()
    url_map.clear()
    webhook.clear_logs()
    return "Logs and URL map cleared", 200

@app.route('/logs')
def get_logs():
    password = os.environ.get('password', 'fake_password')
    input_password = request.args.get('password', '')
    log.append(f'get_logs: timestamp={datetime.datetime.now().isoformat()}')
    if input_password != password:
        return "Unauthorized", 401
    return "<br>".join(log)

@app.route('/redirect')
def redirect_to_index():
    url = request.args.get('url', 'https://example.com')
    code = request.args.get('code', 302)
    mode = request.args.get('mode', 'plain')
    shift = request.args.get('shift', 13)

    log.append(f'redirect_to_index: url={url}, code={code}, mode={mode}, shift={shift}, timestamp={datetime.datetime.now().isoformat()}')

    if ('code' in request.args and request.args['code'].isdigit() and
        int(request.args['code']) in [301, 302, 303, 307, 308]):
        code = int(request.args['code'])
    else:
        code = 302

    converter = URLConverter(url, mode, shift)
    url = converter.convert()

    return redirect(url, code=code)

@app.route('/webhook/')
def webhook_index():
    return render_template('webhook.html')

@app.route('/webhook/create_webhook', methods=['POST'])
def create_webhook():
    webhook_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    webhook.create_webhook(webhook_id)
    time.sleep(0.5)
    log.append(f'add_webhook: webhook_id={webhook_id}, timestamp={datetime.datetime.now().isoformat()}')
    return {"webhook_url": URL + '/webhook/' + webhook_id, "webhook_view_url": URL + '/webhook/view/' + webhook_id}


@app.route('/webhook/<webhook_id>', methods=['GET'])
def webhook_catch(webhook_id):
    if webhook_id not in webhook.log:
        return "Webhook ID does not exist", 404
    webhook.add_log(webhook_id, f"URL {request.url} accessed at {datetime.datetime.now().isoformat()}")
    return f"Webhook {webhook_id} received, please check logs at <a href='{URL + "/webhook/view/" + webhook_id}' class='text-bg-600'>{URL + "/webhook/view/" + webhook_id}</a>", 200

@app.route('/webhook/view/<webhook_id>', methods=['GET'])
def view_webhook(webhook_id):
    if webhook_id not in webhook.log:
        return render_template('error.html'), 404
    logs = webhook.log[webhook_id]
    log.append(f'view_webhook: webhook_id={webhook_id}, timestamp={datetime.datetime.now().isoformat()}')
    return render_template('webhook_view.html', webhook_url=URL + '/webhook/' + webhook_id, logs=logs)

@app.route('/health_check')
def health_check():
    log.append(f'health_check: timestamp={datetime.datetime.now().isoformat()}')
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
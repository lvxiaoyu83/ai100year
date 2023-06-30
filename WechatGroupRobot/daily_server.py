import os
import datetime
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
from pachong2 import get_wechat_artile_content

from db import get_database
_ = load_dotenv(find_dotenv()) # read local .env file
api_key  = os.getenv('DKEY')
server  = os.getenv('SERVER')
port  = os.getenv('PORT')
db = get_database()

app = Flask(__name__)

@app.before_request
def check_key():
    # Check if the client has a valid key.
    if not request.headers.get("Authorization"):
        return "no key"

    # Get the key from the request headers.
    key = request.headers.get("Authorization")

    # Check if the key is valid.
    if key != api_key:
        return "invalid key"

    # The key is valid, so continue with the request.

@app.route("/")
def hello_world():
    return "no"

@app.route("/add_url", methods=['POST'])
def add_url():
    url = request.json.get("url")
    if not db.check_url(url):
        print(url)
        hao, title, desc, ctt = get_wechat_artile_content(url)
        if hao:
            db.create('article', {
                'title': title,
                'hao': hao,
                'url': url,
                'desc': desc,
                'abst': '',
                'ctt': ctt
            })
            return {'title': title}
    return {}

@app.route("/articles", methods=['POST'])
def articles():
    url = request.json.get("url")
    res = {}
    if url == 'xxx':
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        res['data'] = db.read('article', ' hao, title, ctime ', f"ctime > '{current_date}' ")
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
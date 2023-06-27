import os
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv

from db import SqliteDb
_ = load_dotenv(find_dotenv()) # read local .env file
api_key  = os.getenv('DKEY')

db = SqliteDb('test.sqlite')
db.create_table('article', 'hao TEXT, title TEXT, url TEXT, desc TEXT, abst TEXT, ctt TEXT')

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
        db.create('article', {
            'title': '',
            'hao': '',
            'url': url,
            'desc': '',
            'abst': '',
            'ctt': ''
        })
    return {}

if __name__ == "__main__":
    app.run(host='0.0.0.0', post='3389')
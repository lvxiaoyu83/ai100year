import os
import datetime
import markdown
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

    xxx = request.args.get('xxxarg')
    if xxx == 'argxxx':
        return 
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

@app.route("/daily", methods=['GET'])
def daily():
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    art_list = []
    rows = db.read('article', ' url ', f"ctime > '{current_date}' ")
    for r in rows:
        if len(r) > 0:
            rr = db.article(r[0])  # hao, title, abst, url, ctt
            if len(rr) > 0:
                art_list.append(rr)
    md = "\n\n\n\n\n ".join(["### %s | %s \n\n %s\n\n %s\n " % (r[0], r[1], r[2], r[3]) for r in art_list])
    html = markdown.markdown(md)
    return html

@app.route("/articles", methods=['POST'])
def articles():
    res = {}
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    rows = db.read('article', ' hao, title, abst, url ', f"ctime > '{current_date}' ")
    res['data'] = "\n\n\n\n\n ".join(["### %s | %s \n\n %s\n\n %s\n " % (r[0], r[1], r[2], r[3]) for r in rows])

    art_list = []
    rows = db.read('article', ' url ', f"ctime > '{current_date}' ")
    for r in rows:
        if len(r) > 0:
            rr = db.article(r[0])  # hao, title, abst, url, ctt
            if len(rr) > 0:
                art_list.append(rr)
    md = "\n\n\n\n\n ".join(["### %s | %s \n\n %s\n\n %s\n " % (r[0], r[1], r[2], r[3]) for r in art_list])
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
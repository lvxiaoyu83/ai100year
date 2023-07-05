import os
import datetime
from markdown2 import Markdown
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
from pachong2 import get_wechat_artile_content
from db import db, fetch

_ = load_dotenv(find_dotenv()) # read local .env file
api_key  = os.getenv('DKEY')
server  = os.getenv('SERVER')
port  = os.getenv('PORT')
markdowner = Markdown()

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

def article_content(url):
    hao, title, desc, ctt = None, None, None, None
    if not db.check_url(url):
        print(f"fetch from web: {url}")
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
    else:
        hao, title, desc, ctt = db.read('article', ' hao,title,desc,ctt ', f"url='{url}' ")[0]
    return hao, title, desc, ctt

@app.route("/add_url", methods=['POST'])
def add_url():
    url = request.json.get("url")
    if not db.check_url(url):
        print(f"fetch from web: {url}")
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
        else:
            return {} # 数据库里也没有，网络获取也不成功
    else:
        hao, title, desc, ctt = db.read('article', ' hao,title,desc,ctt ', f"url='{url}' ")[0]
    
    hao_index = request.json.get("hao_index")
    article_index = request.json.get("article_index")
    if hao_index is not None and article_index is not None:
        if not db.check_url_index(url):
            db.create('article_index', {
                'article_index': article_index,
                'hao_index': hao_index,
                'url': url
            })
        else:
            query = f"UPDATE article_index SET article_index = {article_index}, hao_index = {hao_index} WHERE url = '{url}'"
            db.execute(query)
            db.commit()
    return {'title': title}

@app.route("/daily", methods=['GET'])
def daily():
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    art_list = []
    rows = db.read('article', ' url ', f"ctime >= '{current_date}' ")
    for r in rows:
        if len(r) > 0:
            rr = db.article(r[0])  # hao, title, abst, url, ctt
            if len(rr) > 0:
                art_list.append(rr[0])
    md = "\n\n\n\n\n".join([f"#### {a[0]} | {a[1]} \n\n{a[2]} \n\n[{a[3]}]({a[3]}) \n\n\n\n " for a in art_list])
    
    html = markdowner.convert(md)
    md = f'<html> <body> ' + md + f' </body> </html>'
    return html

@app.route("/daily2", methods=['GET'])
def daily2():
    md = ''
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    for h in fetch(f"select hao_index from article_index where ctime>='{current_date}' order by hao_index;"):
        art_list = []
        hao_str = ''
        for r in fetch(f"select url from article_index where ctime>='{current_date}' and hao_index='{h[0]}' order by article_index;"):
            url = r[0]
            hao, title, desc, ctt = article_content(url) # todo ctt to abst
            if hao:
                art_list.append([hao, title, desc, url])
                if not hao_str:
                    hao_str = hao
        md += f"### {hao}\n\n"
        md += "\n\n\n\n\n".join([f"#### {a[1]} \n\n{a[2]} \n\n[{a[3]}]({a[3]}) \n\n\n\n " for a in art_list])
        md += "\n\n\n\n\n"
    html = markdowner.convert(md)
    md = f'<html> <body> ' + md + f' </body> </html>'
    return html

@app.route("/articles", methods=['POST'])
def articles():
    res = {}
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    rows = db.read('article', ' hao, title, abst, url ', f"ctime > '{current_date}' ")
    res['data'] = rows
    # res['data'] = "\n\n\n\n\n ".join(["### %s | %s \n\n %s\n\n %s\n " % (r[0], r[1], r[2], r[3]) for r in rows])

    # art_list = []
    # rows = db.read('article', ' url ', f"ctime > '{current_date}' ")
    # for r in rows:
    #     if len(r) > 0:
    #         rr = db.article(r[0])  # hao, title, abst, url, ctt
    #         if len(rr) > 0:
    #             art_list.append(rr)
    # md = "\n\n\n\n\n ".join(["### %s | %s \n\n %s\n\n %s\n " % (r[0], r[1], r[2], r[3]) for r in art_list])
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
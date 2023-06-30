import os
import requests
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
api_key  = os.getenv('DKEY')

server  = os.getenv('SERVER')
port  = os.getenv('PORT')

server_url = f"http://{server}:{port}/add_url"
headers = {"Authorization": api_key}


def post_request(url, data):
    print(url)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("API request failed")

def add_url_to_server(url):
    try:
        if url.startswith("https://"):
            res = post_request(server_url, {"url": url})
            print(f'add_url_to_server {res}')
    except:
        pass

if __name__ == "__main__":
    # add_url_to_server('https://mp.weixin.qq.com/s/7eah_qMhol4EBwrz1bzxeA')
    print(post_request(f"http://{server}:{port}/articles", {"url": 'xxx'}))
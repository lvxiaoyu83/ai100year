import os
import requests
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
api_key  = os.getenv('DKEY')

server  = os.getenv('SERVER')
port  = os.getenv('PORT')

headers = {"Authorization": api_key}


def post_request(url, data):
    print(url)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("API request failed")

def add_url_to_server(url, hao_index, article_index):
    try:
        if url.startswith("https://"):
            res = post_request(f"http://{server}:{port}/add_url", {"url": url, "hao_index": hao_index, "article_index": article_index})
            print(f'add_url_to_server {res}')
    except:
        pass

if __name__ == "__main__":
    add_url_to_server("https://mp.weixin.qq.com/s/UbkKk-0DfPtxNjuBixqDNQ", '0', '0')

    print(post_request(f"http://{server}:{port}/daily2", {}))
    res = requests.get(f"http://{server}:{port}/daily2", headers=headers)
    print(res)
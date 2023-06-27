import os
import requests
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
api_key  = os.getenv('DKEY')

server_url = "http://47.74.43.230:3389/add_url"
headers = {"Authorization": api_key}


def post_request(url, data):
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("API request failed")

def add_url_to_server(url):
    try:
        print(post_request(server_url, {"url": url}))
    except:
        pass
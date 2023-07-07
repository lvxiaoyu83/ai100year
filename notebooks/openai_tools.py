import openai
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.getenv('OPENAI_API_KEY')
openai.api_base = "https://api.openai-proxy.com/v1"
print(openai.api_key)
print(openai.api_base)


def resetapi():
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k",
      messages=[  {'role':'user', 'content': "你好"}  ]
    )
    print(response.id," : ",response.choices[0].message.content)

def call_with_sys(sys_content, user_content_text, max_tokens=2048):
  print(openai.api_base)
  msg = [  
          {'role':'system', 'content': sys_content},
          {'role':'user', 'content': sys_content + "\n\n\n" +user_content_text}  ]
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k", messages=msg,
      temperature=1, max_tokens=max_tokens,
      frequency_penalty=1, presence_penalty=1,
  )
  # print(response.id,":\n",response.choices[0].message.content)
  return response.id, response.choices[0].message.content

def call_completion(user_content_text):
  print(openai.api_base)
  msg = [
          {'role':'user', 'content': user_content_text}  ]
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k", messages=msg,
      temperature=1, max_tokens=2048,
      frequency_penalty=1, presence_penalty=1,
  )
#   print(response.id,":\n",response.choices[0].message.content)
  return response.id, response.choices[0].message.content


resetapi()
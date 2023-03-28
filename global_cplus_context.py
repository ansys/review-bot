"""
This example script demonstrates how to use the OpenAI chat API.

GPT-4 model:
https://platform.openai.com/docs/models/gpt-4

Chat completion API:
https://platform.openai.com/docs/guides/chat

"""
import openai
import secrets
import os

# CSEBU token
token = os.environ.get('TOKEN')

openai.api_key = token 


prompt = """

Create a c++ class using this democode

"""

file_list = ['ParentClass.h','ParentClass.cpp','ChildClass.h','ChildClass.cpp']

for file in file_list:
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    prompt += data


response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
        {"role": "system", "content": "You are a very kind programmer."},
        {"role": "user", "content": prompt},
        # {"role": "assistant", "content": init_response},
        # {"role": "user", "content": elab}
    ]
)

text = response['choices'][0].message.content
print(text)

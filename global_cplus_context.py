"""
This example script demonstrates how to use the OpenAI chat API.

GPT-4 model:
https://platform.openai.com/docs/models/gpt-4

Chat completion API:
https://platform.openai.com/docs/guides/chat

"""
import openai

# CSEBU token
openai.api_key = "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"


prompt = """

Create a c++ class using this democode

"""

with open('GlobalContextClass.h', 'r') as file:
    data = file.read().replace('\n', '')
prompt += data

with open('GlobalContextClass.cpp', 'r') as file:
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

"""
This example script demonstrates how to use the OpenAI chat API.

GPT-4 model:
https://platform.openai.com/docs/models/gpt-4

Chat completion API:
https://platform.openai.com/docs/guides/chat

"""

import secrets
import os
import sys
import openai

if not os.environ.get('TOKEN'):
    print('TOKEN environment variable is not defined.')
    sys.exit(1)
    
# CSEBU token
token = os.environ.get('TOKEN')

openai.api_key = token 

sample_code = """
   int functionA() 
    {
        int num = 5;
        while (num < 10) {
            std::cout << num << std::endl;
            num--; 
        }
        return 0;
    }
"""

prompt_query1 = """"
    Please review the sample_code for logical mistakes and don't add comments on the context_code
    """

prompt_query2 = """"
    Please review the sample_code for readability and logical mistakes based on the context_code provided and don't write the context_code
    and give suggestions for the sample_code only
    """
    
prompt = prompt_query1

prompt += "context_code:"
file_list = ['ParentClass.h','ParentClass.cpp','ChildClass.h','ChildClass.cpp']

for file in file_list:
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    prompt += data

prompt += "some basic rules to check:"
prompt += "comments"
prompt += "public in front of constructor"

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
        {"role": "system", "content": "You are a very kind reviewer."},
        {"role": "user", "content": prompt + sample_code},
        # {"role": "assistant", "content": init_response},
        # {"role": "user", "content": elab}
    ]
)

text = response['choices'][0].message.content
print(text)

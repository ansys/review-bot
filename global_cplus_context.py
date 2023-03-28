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
    sys.exit(0)
    
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
    Please review the sample_code for logical mistakes and don't add any comments for the context_code
    """

prompt_query2 = """"
    Please review the sample_code for readability and logical mistakes based on the context_code provided and don't write the context_code
    and give suggestions for the sample_code only
    """
file_list = ['ParentClass.h','ParentClass.cpp','ChildClass.h','ChildClass.cpp']

def generate_prompt(prompt_query: str, file_list: list) -> str:
    prompt = prompt_query
    
    prompt += "context_code:"
    for file in file_list:
        with open(file, 'r') as file:
            data = file.read().replace('\n', '')
        prompt += data
    
    prompt += "some basic rules to check:"
    prompt += "comments"
    prompt += "public in front of constructor"
    
    return prompt

def call_openai(prompt: str, sample_code: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a kind reviewer."},
            {"role": "user", "content": prompt + sample_code},
            # {"role": "assistant", "content": init_response},
            # {"role": "user", "content": elab}
        ]
    )

    text = response['choices'][0].message.content
    print(text)


print("----------------------------LOGICAL ISSUES: ----------------------------------------")
prompt = generate_prompt(prompt_query1, file_list)
call_openai(prompt,sample_code)

print("----------------------------READABILITY ENHANCEMENT: ----------------------------------------")
prompt = generate_prompt(prompt_query2, file_list)
call_openai(prompt,sample_code)



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

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
DST_FOLDER_OUTPUT = THIS_DIR + '/git_diff_output/'

if not os.environ.get('TOKEN'):
    print('TOKEN environment variable is not defined.')
    sys.exit(0)
    
# CSEBU token
token = os.environ.get('TOKEN')

openai.api_key = token 


prompt_query1 = """"
    Please review the sample_code for logical mistakes and only comment on these and don't output any readability suggestions
    """

prompt_query2 = """"
    Please review the sample_code for readability and give suggestions for the sample_code only
    """
    
os.chdir(DST_FOLDER_OUTPUT)
file_list = os.listdir(os.curdir)  
  
# file_list = ['diff_output2.txt']

def generate_prompt(prompt_query: str, file: str) -> str:
    prompt = prompt_query
    
    prompt += "sample_code:"
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    prompt += data
    
    #prompt += "some basic rules to check:"
    #prompt += "comments"
    #prompt += "public in front of constructor"
    
    return prompt

def call_openai(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a kind c++ reviewer."},
            {"role": "user", "content": prompt},
            # {"role": "assistant", "content": init_response},
            # {"role": "user", "content": elab}
        ]
    )

    text = response['choices'][0].message.content
    #print(text)


print("----------------------------LOGICAL ISSUES: ----------------------------------------")

for item in file_list:
    if not os.path.isfile(item):
        continue
        
    source_file =  DST_FOLDER_OUTPUT + item
    file_size = os.path.getsize(item)
    if os.stat(source_file).st_size == 0 or os.stat(source_file).st_size > 3000:
        continue
    print(f'{item}: {file_size}')
     
    prompt = generate_prompt(prompt_query1, source_file)
    print(prompt)
    call_openai(prompt)

#print("----------------------------READABILITY ENHANCEMENT: ----------------------------------------")
#prompt = generate_prompt(prompt_query2, file_list)
#call_openai(prompt)



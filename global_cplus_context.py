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

prompt_query_for_split_file = """"
       Please review the sample_code for logical mistakes and don't include logical mistakes when it happens in the last line in the file and only comment on these and don't output any readability suggestions
    """
    
os.chdir(DST_FOLDER_OUTPUT)
file_list = os.listdir(os.curdir)  
  
#file_list = ['PrimeFileIO.cpp.gitdiff.txt_split_file_700.txt']
MAX_FILE_SIZE = 8000 # 8000

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
            {"role": "system", "content": "You are a kind c++ reviewer giving very short answers."},
            {"role": "user", "content": prompt},
            # {"role": "assistant", "content": init_response},
            # {"role": "user", "content": elab}
        ]
    )

    text = response['choices'][0].message.content
    print(text)
    print("\n")


print("---------------------------------------- LOGICAL ISSUES: ----------------------------------------")

index = 0
for item in file_list:
    if not os.path.isfile(item):
        continue
    index = index + 1
    #if index > 1:
    #    continue  
     
    file_size = os.path.getsize(item)
    print("----------------------------------------------------------------------------------------------------")
    print(f'{item}: {file_size}')
    
    substring = ".h"
    if substring in item:
        print(f'ChatGPT cannot analyse logical issues in Header files')
        continue
          
    source_file =  DST_FOLDER_OUTPUT + item
       
    list_small_files = list()
    
    if os.stat(source_file).st_size > MAX_FILE_SIZE:
        print(f'{item}: BIG FILE')
        lines_per_file = 700
        smallfile = None
        split_file = source_file
        with open(split_file) as bigfile:
            for lineno, line in enumerate(bigfile):
                if lineno % lines_per_file == 0:
                    if smallfile:
                        smallfile.close()
                    small_filename = item + '_split_file_{}.txt'.format(lineno + lines_per_file)
                    smallfile = open(small_filename, "w")
                    list_small_files.append(small_filename)
                smallfile.write(line)
            if smallfile:
                smallfile.close()
                
    elif os.stat(source_file).st_size == 0:
        continue
    
    if len(list_small_files) == 0:
        prompt = generate_prompt(prompt_query1, source_file)
        call_openai(prompt)
    else:
       for small_source_file in list_small_files: 
           print(f'split_file {item}: {small_source_file}')
           prompt = generate_prompt(prompt_query_for_split_file, small_source_file)
           call_openai(prompt)
           # os.remove(small_source_file)




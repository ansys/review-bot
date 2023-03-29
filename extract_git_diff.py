
#!/usr/bin/python3

import os
import shutil
import subprocess
import pandas as pd
import numpy as np
import string
import enum
from typing import List, Optional


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
FILE_DIR = THIS_DIR + '/mesh/'
DST_FOLDER_OUTPUT = THIS_DIR + '/git_diff_output/'

def git_diff_per_file(in_list: list):
    numb = len(in_list)
    print(f'Number of files: {numb}')
    data = pd.DataFrame(columns=['code_files','size'], index=range(numb))
    
    index = 0
    for item in in_list:
        if not os.path.isfile(item):
            continue
        print(f'{index}: {item}')
        
        source = FILE_DIR + item
        output = DST_FOLDER_OUTPUT + item + ".gitdiff.txt"
        cmd = (
                "git diff master 2e7237f "
                f"{source} "
                f"> {output} "
        )
        os.system(cmd)
  
        
def main():
    print(f'directory {FILE_DIR}')
    if not os.path.exists(FILE_DIR):
        print('File structure not as expected!\n')
        return
    
    dst = os.path.join(THIS_DIR, DST_FOLDER_OUTPUT )
    if not os.path.exists(dst):
        os.makedirs(DST_FOLDER_OUTPUT)

    os.chdir(FILE_DIR)
    git_diff_per_file(os.listdir(os.curdir))

 
    exit(0)

if __name__ == '__main__':
    main() 
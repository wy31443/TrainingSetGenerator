
from collections import deque
import os
import random

def get_list_of_files() -> deque:
    base_folder = os.path.join(os.getcwd(), 'processed')
    folders = os.listdir(base_folder)
    all_files = dict()
    # Iterate over all the entries
    for folder in folders:
        stack = deque()
        subfolder = os.path.join(base_folder, folder)
        if os.path.isdir(subfolder):
            images = os.listdir(os.path.join(base_folder, folder))
            for image in images:
                stack.append(image)
            all_files[folder] = stack
                
    return all_files

res = get_list_of_files()
folder = random.choice(list(res.keys()))
frame = random.choice(res[folder])
filepath = os.path.join(os.getcwd(), 'processed', folder, frame)
print(filepath)
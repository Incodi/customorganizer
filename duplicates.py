import os
import sys
from pathlib import Path
import hashlib

def find_duplicates(folder):
    Duplic = {}
    for dirpath, dirnames, filenames in os.walk(folder):
        # Avoids treating folders as files but as directories!
        dirnames[:] = [d for d in dirnames if "." not in d]
        for file_name in filenames:
            path = os.path.join(dirpath, file_name)
                
            file_hash = Hash_File(path)
            if file_hash in Duplic:
                Duplic[file_hash].append(path)  # Store full path
            else:
                Duplic[file_hash] = [path]
    return Duplic

def Join_Dictionary(dict1, dict2):
    for key in dict2:
        dict1[key] = dict1.get(key, []) + dict2[key]

def Hash_File(path):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

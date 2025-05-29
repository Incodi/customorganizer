import os
import sys
from pathlib import Path
import hashlib

'''
Based on code from Geeks for Geeks
https://www.geeksforgeeks.org/finding-duplicate-files-with-python/
'''


def FindDuplicate(folder):
    Duplic = {}
    for file_name in os.listdir(folder):
        path = os.path.join(folder, file_name)
        
        # Skip directories
        if not os.path.isfile(path):
            continue
            
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

if __name__ == "__main__":
    target_folder = Path('/Users/c/Downloads') 
    if not target_folder.exists():
        print(f"Error: Folder {target_folder} does not exist")
        sys.exit(1)

    duplicates = FindDuplicate(target_folder)

    results = [files for files in duplicates.values() if len(files) > 1]
    
    if results:
        print("Duplicate files found:")
        for group in results:
            print("\nThese files are identical:")
            for file in group:
                print(f" - {file}")
    else:
        print("No duplicates found.")
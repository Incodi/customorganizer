import os
from pathlib import Path
import shutil

def save_undo_log(directory):
    with open(Path(directory) / "undo_log.txt", "w") as f:
        for file in Path(directory).rglob("*.*"):
            if file.name != "undo_log.txt":
                f.write(f"{file.parent}|{file.name}\n")

def undo_last_organization(directory):
    undo_file = Path(directory) / "undo_log.txt"
    if undo_file.exists():
        with open(undo_file) as f:
            for line in f:
                path, filename = line.strip().split("|")
                shutil.move(Path(path).joinpath(filename), Path(directory))

directories = {
    "ArtsandMemes": [".jpeg", ".jpg", ".gif", ".png", ".webp", ".xcf", 
                     ".psd", ".ora", ".scriv", ".toml", ".gba", ".procreate", 
                     ".artstudio", ".odp", ".heic"],
    "Videos": [".wmv", ".mov", ".mp4", ".mpg", ".mpeg", ".mkv"], 
    "Zips": [".iso", ".tar", ".gz", ".rz", ".7z", ".dmg", ".rar", ".zip"],
    "Audio": [".mp3", ".msv", ".wav", ".wma"],
    "PDFs": [".pdf"],
}

File_Format_Dictionary = {
    final_file_format: directory
    for directory, file_format_stored in directories.items()
    for final_file_format in file_format_stored
}

def organizer(target_directory):
    target_path = Path(target_directory)
    others = target_path / "Others"
    os.makedirs(others, exist_ok=True)
    
    for entry in os.scandir(target_directory):
        if entry.is_dir():
            continue
            
        file_path = Path(entry)
        final_file_format = file_path.suffix.lower()
        
        if file_path.name == "undo_log.txt":
            continue

        if final_file_format in File_Format_Dictionary:
            directory_path = target_path / File_Format_Dictionary[final_file_format]
            os.makedirs(directory_path, exist_ok=True)
            try:
                os.rename(file_path, directory_path / file_path.name)
            except OSError as e:
                print(f"Failed to move {file_path}: {e}")
        elif final_file_format == ".py":
            continue
        else:
            # Move to Others if extension not recognized
            try:
                os.rename(file_path, others / file_path.name)
            except OSError as e:
                print(f"Failed to move {file_path} to Others: {e}")

if __name__ == "__main__":
    # Example input: /Users/c/Downloads
    target_dir = input("Enter the directory path to organize (or press Enter for current directory): ").strip()
    if not target_dir:
        target_dir = os.getcwd()
    
    if not Path(target_dir).exists():
        print(f"Directory '{target_dir}' does not exist!")
    else:
        save_undo_log(target_dir)
        organizer(target_dir)
        print(f"Organization complete in: {target_dir}")

import os
from pathlib import Path
import shutil

def save_undo_log():
    """Save current file positions for undo"""
    with open("undo_log.txt", "w") as f:
        for file in Path.cwd().rglob("*.*"):
            f.write(f"{file.parent}|{file.name}\n")

def undo_last_organization():
    """Revert last organization"""
    if Path("undo_log.txt").exists():
        with open("undo_log.txt") as f:
            for line in f:
                path, filename = line.strip().split("|")
                shutil.move(Path(path).joinpath(filename), Path.cwd())

directories = {
    "ArtsandMemes": [".jpeg", ".jpg", ".gif", ".png", ".webm", ".xcf", 
                     ".psd", ".ora", ".scriv", ".toml", ".gba", ".procreate", 
                     ".artstudio", ".odp"],
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

def organizer():
    others = Path("Others")
    os.makedirs(others, exist_ok=True)
    
    for entry in os.scandir():
        if entry.is_dir():
            continue
            
        file_path = Path(entry)
        final_file_format = file_path.suffix.lower()
        
        if final_file_format in File_Format_Dictionary:
            directory_path = Path(File_Format_Dictionary[final_file_format])
            os.makedirs(directory_path, exist_ok=True)
            try:
                os.rename(file_path, directory_path.joinpath(file_path))
            except OSError as e:
                print(f"Failed to move {file_path}: {e}")
        elif final_file_format == ".py":
            continue
        else:
            # Move to Others if extension not recognized
            try:
                os.rename(file_path, others.joinpath(file_path))
            except OSError as e:
                print(f"Failed to move {file_path} to Others: {e}")

if __name__ == "__main__":
    organizer()
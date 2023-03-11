import os
import time
from pathlib import Path
import shutil

src_path = Path().resolve().parent
print("src_path:", src_path)
src_dir_name = src_path.name
print("src_dir_name:", src_dir_name)

root_path = src_path.parent
print("root_path:", root_path)
dst_dir_list = []
root_list = os.listdir(root_path)
for file in root_list:
    path = root_path.joinpath(file)
    isdir = os.path.isdir(path)
    if isdir and src_dir_name in file and not file == src_dir_name:
        print(path)
        dst_dir_list.append(path)

src_list = os.listdir(src_path)
ignore_list = [
    ".git",
    "__pycache__",
    "caches",
    "install",
    ".gitignore",
    "temp_screenshot",
]

for src_file in src_list:
    if src_file not in ignore_list:
        src_file_path = src_path.joinpath(src_file)
        isdir = os.path.isdir(src_file_path)
        for dst_dir_path in dst_dir_list:
            if isdir:
                dst_file_path = dst_dir_path.joinpath(src_file)
                if os.path.exists(dst_file_path):
                    shutil.rmtree(dst_file_path)
                shutil.copytree(src_file_path, dst_file_path)
            else:
                shutil.copy(src_file_path, dst_dir_path)

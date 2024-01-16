import os
from os import path
import sys

ml_dir = path.abspath(path.join(path.dirname(__file__), os.pardir))
src_dir = path.abspath(path.join(ml_dir, os.pardir))
entry_dir = src_dir.replace("/src", "")
sys.path.append(entry_dir)

print(f'ml_dir: {ml_dir} | src_dir: {src_dir} | entry_dir: {entry_dir} \n\n')

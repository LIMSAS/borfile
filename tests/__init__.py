import os

from .utils import glob_bor_files

INPUT_FILES_DIR = os.path.join(os.path.dirname(__file__), "data")

INPUT_BOR_FILES = glob_bor_files(INPUT_FILES_DIR)

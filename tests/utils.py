# coding: utf-8
import pathlib


def glob_bor_files(data_dir):
    files = list(pathlib.Path(data_dir).rglob("*.bor"))
    return sorted(set(files), key=lambda x: x.name)

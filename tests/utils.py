import filecmp
import pathlib
import shutil


def glob_bor_files(data_dir):
    files = list(pathlib.Path(data_dir).rglob("*.bor"))
    return sorted(set(files), key=lambda x: x.name)


def assert_same_files(f1, f2, copy_if_missing=True):
    if copy_if_missing and not f2.exists():
        shutil.copy(f1, f2)
    fpath1, fpath2 = f1.as_posix(), f2.as_posix()
    assert filecmp.cmp(fpath1, fpath2), f"{fpath1} != {fpath2}"

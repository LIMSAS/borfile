# -*- coding: utf-8 -*-
import random
from pathlib import Path

import pandas.testing
import pytest
import xarray
import xarray.testing
from pytest_cases import pytest_fixture_plus

import bor

from . import INPUT_BOR_FILES, INPUT_FILES_DIR


@pytest_fixture_plus(
    scope="function",
    params=INPUT_BOR_FILES,
    ids=[p.relative_to(INPUT_FILES_DIR).as_posix() for p in INPUT_BOR_FILES],
)
def bor_file(request):
    if request.param.as_posix().lower().endswith(".bor"):
        bor_file = bor.read(request.param)
        return bor_file


def test_edit_dataframe_and_dataset(bor_file):
    random_int = random.randint(1, 1000)
    first_index = bor_file.data.index[0]
    first_variable = bor_file.data.columns[0]
    bor_file.data.loc[first_index, first_variable] = random_int
    assert (
        int(bor_file.to_dataset().sel(time=first_index)[first_variable]) == random_int
    )


def test_compare_dataframe_and_dataset(bor_file):
    pandas.testing.assert_frame_equal(
        bor_file.to_dataset().to_dataframe(), bor_file.data
    )


def test_compare_dataset_and_dataframe(bor_file):
    xarray.testing.assert_equal(bor_file.to_dataset(), bor_file.data.to_xarray())


def test_compare_metadata(bor_file):
    assert not hasattr(bor_file, "_dataframe")
    ds = xarray.open_dataset(bor_file.data_nc)
    assert not hasattr(bor_file, "_dataframe")
    for var in list(ds.variables):
        ds[var].attrs == bor_file.metadata[var]

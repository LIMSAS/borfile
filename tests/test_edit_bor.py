# -*- coding: utf-8 -*-
import random
from pathlib import Path

import pytest
from pytest_cases import pytest_fixture_plus

import borfile

from . import INPUT_BOR_FILES, INPUT_FILES_DIR


@pytest_fixture_plus(
    scope="function",
    params=INPUT_BOR_FILES,
    ids=[p.relative_to(INPUT_FILES_DIR).as_posix() for p in INPUT_BOR_FILES],
)
def bor_file(request):
    if request.param.as_posix().lower().endswith(".bor"):
        bor_file = borfile.read(request.param)
        return bor_file


def test_edit_description(bor_file, request):
    new_project_ref = "PROJECT REF {}".format(request.node.callspec.id)
    assert new_project_ref not in bor_file.description_xml

    bor_file.description["project_ref"] = new_project_ref
    assert new_project_ref in bor_file.description_xml

    bor_file.reset()
    assert new_project_ref not in bor_file.description_xml


def test_edit_dataframe(bor_file, request):
    assert bor_file.data.shape[0] > 1
    bor_file.data = bor_file.data.iloc[:1]
    assert bor_file.data.shape[0] == 1

    bor_file.reset()
    assert bor_file.data.shape[0] > 1

    num_variables = len(bor_file.data.columns)
    variable_to_drop = list(bor_file.data.columns)[1]

    # drop do not update data inplace
    bor_file.data.drop(columns=[variable_to_drop])
    assert len(bor_file.data.columns) == num_variables

    # Update in place
    bor_file.data.drop(columns=[variable_to_drop], inplace=True)
    assert len(bor_file.data.columns) == (num_variables - 1)
    bor_file.reset()

    # set new dataframe
    bor_file.data = bor_file.data.drop(columns=[variable_to_drop])
    assert len(bor_file.data.columns) == (num_variables - 1)
    bor_file.reset()
    assert len(bor_file.data.columns) == num_variables

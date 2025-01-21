# -*- coding: utf-8 -*-
import pytest
from pytest_cases import pytest_fixture_plus

import bor

from . import INPUT_BOR_FILES, INPUT_FILES_DIR
from .utils import assert_same_files


@pytest_fixture_plus(
    scope="function",
    params=INPUT_BOR_FILES,
    ids=[p.relative_to(INPUT_FILES_DIR).as_posix() for p in INPUT_BOR_FILES],
)
def bor_file(request):
    if request.param.as_posix().lower().endswith(".bor"):
        bor_file = bor.read(request.param)
        return bor_file


def test_csv_export(bor_file, tmp_path):
    csv_output_filename = tmp_path / "output.csv"
    bor_file.to_csv(csv_output_filename)
    assert_same_files(csv_output_filename, bor_file._source_file.with_suffix(".csv"))


def test_json_export(bor_file, tmp_path):
    json_output_filename = tmp_path / "output.json"
    bor_file.to_json(json_output_filename, indent=2)
    assert_same_files(json_output_filename, bor_file._source_file.with_suffix(".json"))


def test_xml_export(bor_file, tmp_path):
    xml_output_filename = tmp_path / "output.xml"
    bor_file.to_xml(xml_output_filename)
    assert_same_files(xml_output_filename, bor_file._source_file.with_suffix(".xml"))


def test_parquet_export(bor_file, tmp_path):
    parquet_output_filename = tmp_path / "output.parquet"
    bor_file.to_parquet(parquet_output_filename)
    assert_same_files(
        parquet_output_filename, bor_file._source_file.with_suffix(".parquet")
    )

# -*- coding: utf-8 -*-
from pathlib import Path

import pytest
from pytest_cases import pytest_fixture_plus

import bor

from . import INPUT_BOR_FILES, INPUT_FILES_DIR


@pytest_fixture_plus(
    scope="module",
    params=INPUT_BOR_FILES,
    ids=[p.relative_to(INPUT_FILES_DIR).as_posix() for p in INPUT_BOR_FILES],
)
def bor_file(request):
    if request.param.as_posix().lower().endswith(".bor"):
        return bor.read(request.param)


DRILLING_METHOD_CODES = (
    "DRLMTD_HA",
    "DRLMTD_CFA",
    "DRLMTD_ADM",
    "DRLMTD_HSA",
    "DRLMTD_DTM",
    "DRLMTD_COR",
    "DRLMTD_RTR",
    "DRLMTD_RRFFM",
    "DRLMTD_RTRPRC",
    "DRLMTD_RPM",
    "DRLMTD_DTH",
    "DRLMTD_DRI",
    "DRLMTD_DS",
    "DRLMTD_DST",
    "DRLMTD_STDTM",
    "DRLMTD_CPD",
    "DRLMTD_VDS",
    "DRLMTD_VD",
    "DRLMTD_VS",
    "DRLMTD_PS",
)

DRILLING_PARAMETERS_LOG = (
    "time",
    "DEPTH",
    "AS",
    "EVP",
    "EVR",
    "EVS",
    "TP",
    "IP",
    "TQ",
    "TQC",
    "RSP",
    "RSPC",
    "HP",
    "SP",
    "RV",
    "IF",
    "OF",
    "IV",
    "OV",
    "AP",
    "AF",
    "AV",
    "WF",
    "WP",
    "WV",
    "ECM",
    "PHM",
    "DO2M",
    "TEMPM",
)


PRESSUREMETER_TEST_TYPES = ("ground", "volume_loss", "pressure_loss")

PRESSUREMETER_LOG_NAMES = (
    "time",
    "STEP",
    "PR1",
    "PR15",
    "PR30",
    "PR60",
    "PG1",
    "PG15",
    "PG30",
    "PG60",
    "V1",
    "V15",
    "V30",
    "V60",
    "CREEP",
    "DELT60",
)


def test_description(bor_file):
    assert bor_file.description_xml != ""
    assert "borehole_ref" in bor_file.description
    assert "project_ref" in bor_file.description
    assert "creation" in bor_file.description
    assert "modification" in bor_file.description
    assert "device" in bor_file.description
    assert "filename" in bor_file.description

    assert "convention" in bor_file.description
    assert bor_file.description["convention"]["@version"] in ("1.0", "1.1", "1.2")

    if bor_file.domain == "DRILLING PARAMETERS":
        assert bor_file.description["convention"]["@version"] == "1.1"
        assert bor_file.description["convention"]["parameters"]["@phase"] == "DRILL"
        assert bor_file.description["convention"]["parameters"]["logfile"] == "data.nc"
        assert "drilling" in bor_file.description
        if "method" in bor_file.description["drilling"]:
            assert bor_file.description["drilling"]["method"] in DRILLING_METHOD_CODES

    if bor_file.domain == "MENARD PRESSUREMETER TEST":
        assert bor_file.description["convention"]["@version"] in ("1.1", "1.2")
        assert "pressuremeter" in bor_file.description["convention"]
        assert any(
            [
                ptt in bor_file.description["convention"]["pressuremeter"]
                for ptt in PRESSUREMETER_TEST_TYPES
            ]
        )


def test_data_nc(bor_file):
    assert bor_file.data_nc
    assert bor_file.data_nc[:3].decode() == "CDF"


def test_dataframe_index(bor_file):
    assert "time" not in bor_file.data
    assert bor_file.data.index.name == "time"


def test_dataset_index(bor_file):
    ds = bor_file.to_dataset()
    assert "time" in ds.variables
    assert list(ds.indexes) == ["time"]


def test_dataframe_parameters(bor_file):
    assert bor_file.data.size > 0
    assert len(bor_file.data.to_dict().keys()) > 0

    assert "time" not in bor_file.data
    assert "time" in bor_file.data.reset_index(drop=False)

    if bor_file.domain == "DRILLING PARAMETERS":
        assert "DEPTH" in bor_file.data
        assert "time" in bor_file.data.reset_index(drop=False)
        for parameter in list(bor_file.data.columns):
            assert parameter in DRILLING_PARAMETERS_LOG

    if bor_file.domain == "MENARD PRESSUREMETER TEST":
        assert "STEP" in bor_file.data
        assert "time" not in bor_file.data
        for parameter in list(bor_file.data.columns):
            assert parameter in PRESSUREMETER_LOG_NAMES


def test_dataset_parameters(bor_file):
    ds = bor_file.to_dataset()
    assert ds.to_array().size > 0
    assert len(list(ds.variables)) > 0

    if bor_file.domain == "DRILLING PARAMETERS":
        assert "DEPTH" in ds.variables
        for parameter in list(ds.variables):
            assert parameter in DRILLING_PARAMETERS_LOG

    if bor_file.domain == "MENARD PRESSUREMETER TEST":
        assert "STEP" in ds.variables
        for parameter in list(ds.variables):
            assert parameter in PRESSUREMETER_LOG_NAMES

from click.testing import CliRunner
from pytest_cases import pytest_fixture_plus

from borfile.cli import convert_to_csv, convert_to_json, convert_to_xml

from . import INPUT_BOR_FILES, INPUT_FILES_DIR
from .utils import assert_same_files


@pytest_fixture_plus(
    scope="function",
    params=INPUT_BOR_FILES,
    ids=[p.relative_to(INPUT_FILES_DIR).as_posix() for p in INPUT_BOR_FILES],
)
def bor_path(request):
    return request.param


def test_bor2csv_output_option(bor_path, tmp_path):
    output = tmp_path / "output.csv"
    result = CliRunner().invoke(convert_to_csv, [str(bor_path), "-o", str(output)])
    assert result.exit_code == 0, result.output
    assert_same_files(output, bor_path.with_suffix(".csv"))


def test_bor2json_output_option(bor_path, tmp_path):
    output = tmp_path / "output.json"
    result = CliRunner().invoke(
        convert_to_json, [str(bor_path), "-o", str(output), "--float-precision", "2"]
    )
    assert result.exit_code == 0, result.output
    assert_same_files(output, bor_path.with_suffix(".json"))


def test_bor2xml_output_option(bor_path, tmp_path):
    output = tmp_path / "output.xml"
    result = CliRunner().invoke(convert_to_xml, [str(bor_path), "-o", str(output)])
    assert result.exit_code == 0, result.output
    assert_same_files(output, bor_path.with_suffix(".xml"))

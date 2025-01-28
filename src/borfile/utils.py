import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

import xarray
import xmltodict


def xml_to_dict(xml_input, cdata_key="value", process_comments=True, **kwargs):
    return xmltodict.parse(
        xml_input,
        cdata_key=cdata_key,
        process_comments=process_comments,
        **kwargs,
    )


def dict_to_xml(dict_input, cdata_key="value", process_comments=True, **kwargs):
    return xmltodict.unparse(
        dict_input,
        cdata_key=cdata_key,
        pretty=True,
        **kwargs,
    )


@contextmanager
def set_directory(path: Path):
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def open_dataset(data_nc, **kwargs):
    if kwargs.get("engine", None) == "netcdf4":
        with tempfile.TemporaryDirectory() as outdir:
            with set_directory(outdir):
                with open("data.nc", "wb") as fd:
                    fd.write(data_nc)
                return xarray.open_dataset("data.nc", **kwargs)
    else:
        return xarray.open_dataset(data_nc, **kwargs)

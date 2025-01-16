# -*- coding: utf-8 -*-
import io
import stat
import tempfile
from datetime import datetime
from zipfile import ZipFile

import stream_zip

from .utils import dict_to_xml, open_dataset, xml_to_dict


def read(bor_filename, **kwargs):
    return BorFile(bor_filename, **kwargs)


class BorFile:

    _domains = {
        "D": "DRILLING PARAMETERS",
        "G": "GROUTING PARAMETERS",
        "J": "JETGROUTING PARAMETERS",
        "P": "MENARD PRESSUREMETER TEST",
        "A": "CONTINUOUS FLIGHT AUGER PILE",
        "L": "LUGEON TEST",
        "V": "VIBROFLOTATION",
        "Y": "DYNAMIC PROBING",
    }

    def __init__(
        self,
        source_file,
        netcdf_format="NETCDF3_CLASSIC",
        netcdf_engine="scipy",
        **kwargs
    ):
        super(BorFile, self).__init__()
        self._netcdf_format = netcdf_format
        self._netcdf_engine = netcdf_engine
        self._source_file = source_file
        if hasattr(self._source_file, "read"):
            self._raw_bytes = self._source_file.read()
        else:
            with open(self._source_file, "rb") as fd:
                self._raw_bytes = fd.read()

    @property
    def description(self):
        if not hasattr(self, "_description"):
            xml = self._extract_file("description.xml", decode=True)
            self._description = xml_to_dict(xml)["description"]
        return self._description

    @property
    def description_xml(self):
        if hasattr(self, "_description"):
            return dict_to_xml({"description": self._description})
        else:
            return self._extract_file("description.xml", decode=True)

    @property
    def data_nc(self):
        if hasattr(self, "_data"):
            return self.to_dataset().to_netcdf(
                format=self._netcdf_format, engine=self._netcdf_engine
            )
        else:
            return self._extract_file("data.nc")

    @property
    def metadata(self):
        if not hasattr(self, "_metadata"):
            self._load_data()
        return self._metadata

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self._load_data()
        return self._data

    @data.setter
    def data(self, df):
        self._data = df
        if df.attrs:
            self._metadata = df.attrs

    @property
    def domain(self):
        domain_id = self.description["filename"][-1].upper()
        return self._domains[domain_id]

    def save(self, target=None, **kwargs):
        def dumps(file_like=None):
            file_like = file_like or io.BytesIO()
            member_files = (
                (
                    "description.xml",
                    datetime.now(),
                    stat.S_IFREG | 0o600,
                    stream_zip.ZIP_32,
                    (self.description_xml.encode(),),
                ),
                (
                    "data.nc",
                    datetime.now(),
                    stat.S_IFREG | 0o600,
                    stream_zip.ZIP_32,
                    (self.data_nc,),
                ),
            )

            for chunk in stream_zip.stream_zip(member_files):
                file_like.write(chunk)
            return file_like

        if target is None:
            target = self._source_file

        if hasattr(target, "write"):
            dumps(target)
        else:
            with open(target, "wb") as fd:
                dumps(fd)

    def reset(self):
        self.__dict__.pop("_data", None)
        self.__dict__.pop("_metadata", None)
        self.__dict__.pop("_description", None)

    def to_dataset(self, *args, **kwargs):
        df = self.data.reset_index(drop=False)
        ds = df.set_index("time").to_xarray()
        ds.encoding = {"unlimited_dims": {"time"}}

        for var in list(ds.variables):
            ds[var].encoding["dtype"] = df[var].dtype
            ds[var].encoding["_FillValue"] = None
            if var in self._metadata:
                ds[var].attrs = self._metadata[var]
        return ds

    def to_csv(self, *args, **kwargs):
        rename_mapping = {}
        for key, value in self.metadata.items():
            if value.get("unit", None):
                rename_mapping[key] = "{} ({})".format(key, value["unit"])

        return (
            self.data.reset_index(drop=False)
            .rename(columns=rename_mapping)
            .set_index(rename_mapping["time"])
            .to_csv(*args, **kwargs)
        )

    def to_dict(self, *args, **kwargs):
        kwargs.setdefault("orient", "records")
        return self.data.to_dict(*args, **kwargs)

    def to_json(self, *args, **kwargs):
        kwargs.setdefault("orient", "records")
        kwargs.setdefault("double_precision", 2)
        return self.data.to_json(*args, **kwargs)

    def to_xml(self, *args, **kwargs):
        return self.data.to_xml(*args, **kwargs)

    def to_parquet(self, *args, **kwargs):
        return self.data.to_parquet(*args, **kwargs)

    def to_zarr(self, *args, **kwargs):
        return self.to_dataset().to_zarr(*args, **kwargs)

    def _load_data(self, **kwargs):
        ds = open_dataset(
            self.data_nc, format=self._netcdf_format, engine=self._netcdf_engine
        )
        self._data = ds.to_dataframe()
        self._metadata = {}
        for var in list(ds.variables):
            self._metadata[var] = ds.variables[var].attrs
        self._data.attrs = self._metadata

    def _extract_file(self, filename, decode=False):
        zip_archive = ZipFile(io.BytesIO(self._raw_bytes))
        file = zip_archive.read(filename)
        return file.decode() if decode else file

    def __repr__(self):
        cls_name = ".".join([self.__module__, self.__class__.__name__])
        return "<{} {}>".format(cls_name, self.description["filename"])

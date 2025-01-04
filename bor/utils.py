# -*- coding: utf-8 -*-
import os
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

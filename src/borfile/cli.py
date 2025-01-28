#!/usr/bin/env python
import click

from .file import BorFile


@click.command()
@click.argument("bor_input", type=click.File("rb"))
@click.option(
    "-o", "--output", type=click.Path(writable=True, dir_okay=False), required=False
)
@click.option(
    "--compact",
    is_flag=True,
    show_default=True,
    default=False,
    help="suppress all whitespace separation (most compact)",
)
@click.option(
    "--float-precision",
    default=1,
    show_default=True,
    help="the number of decimal places to use when encoding floating point values",
)
def convert_to_json(bor_input, output, compact, float_precision):
    """Convert BOR file to a JSON."""
    bor = BorFile(bor_input)
    dump_args = {"indent": None} if compact else {"indent": 2}
    dump_args["double_precision"] = float_precision
    if not output:
        print(bor.to_json(**dump_args))
    else:
        bor.to_json(output, output, **dump_args)

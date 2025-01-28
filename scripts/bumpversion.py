#!/usr/bin/env python


import builtins
import datetime
import os
import re
import subprocess
from argparse import ArgumentParser
from argparse import FileType
from argparse import RawTextHelpFormatter


def generate_changelog_title(version):
    version_title = f"Version {version}"
    return version_title + "\n" + "-" * len(version_title)


def get_release_date():
    dt = datetime.date.today()
    if 4 <= dt.day <= 20 or 24 <= dt.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][dt.day % 10 - 1]
    return dt.strftime(f"%B %d{suffix} %Y")


def bump_release_version(args):
    """Automated software release workflow

      * Bumps the release version number (with .bumpversion.cfg)
      * Preloads the correct changelog template for editing
      * Builds a source distribution
      * Sets release date
      * Tags the release

    You can run it like::

        $ python bumpversion.py

    which will create a 'release' version (Eg. 0.7.2-dev => 0.7.2).

    """
    # Dry run 'bumpversion' to find out what the new version number
    # would be. Useful side effect: exits if the working directory is not
    # clean.
    changelog = args.changelog.name
    bumpver = subprocess.check_output(
        ["bump-my-version", "bump", "release", "--dry-run", "--verbose"],
        stderr=subprocess.STDOUT,
    ).decode("utf-8")
    m = re.search(r"current version.*?'(\d+\.\d+\.\d+\.dev\d+|\d+\.\d+\.\d+)'", bumpver)
    current_version = m.groups(0)[0]
    m = re.search(
        r"New version will be.*?'(\d+\.\d+\.\d+\.dev\d+|\d+\.\d+\.\d+)'", bumpver
    )
    release_version = m.groups(0)[0]

    date = get_release_date()

    current_version_title = generate_changelog_title(current_version)
    release_version_title = generate_changelog_title(release_version)
    changes = ""
    with builtins.open(changelog) as fd:
        changes += fd.read()

    changes = changes.replace(current_version_title, release_version_title).replace(
        "**unreleased**", f"Released on {date}"
    )

    with builtins.open(changelog, "w") as fd:
        fd.write(changes)

    # Tries to load the EDITOR environment variable, else falls back to vim
    editor = os.environ.get("EDITOR", "vim")
    os.system(f"{editor} {changelog}")

    subprocess.check_output(["flit", "build"])

    # Have to add it so it will be part of the commit
    subprocess.check_output(["git", "add", changelog])
    subprocess.check_output(["git", "commit", "-m", f"Changelog for {release_version}"])

    # Really run bumpver to set the new release and tag
    bv_args = ["bump-my-version", "bump", "release"]

    bv_args += ["--new-version", release_version]

    subprocess.check_output(bv_args)


def bump_new_version(args):
    """Increment the version number to the next development version

      * Bumps the development version number (with .bumpversion.toml)
      * Preloads the correct changelog template for editing

    You can run it like::

        $ python bumpversion.py newversion

    which, by default, will create a 'patch' dev version (0.0.1 => 0.0.2-dev).

    You can also specify a patch level (patch, minor, major) to change to::

        $ python bumpversion.py newversion major

    which will create a 'major' release (0.0.2 => 1.0.0-dev)."""

    # Dry run 'bumpversion' to find out what the new version number
    # would be. Useful side effect: exits if the working directory is not
    # clean.
    changelog = args.changelog.name
    part = args.part
    bumpver = subprocess.check_output(
        ["bump-my-version", "bump", part, "--dry-run", "--verbose"],
        stderr=subprocess.STDOUT,
    ).decode("utf-8")
    m = re.search(r"current version.*?'(\d+\.\d+\.\d+\.dev\d+|\d+\.\d+\.\d+)'", bumpver)
    current_version = m.groups(0)[0]
    m = re.search(
        r"New version will be.*?'(\d+\.\d+\.\d+\.dev\d+|\d+\.\d+\.\d+)'", bumpver
    )
    next_version = m.groups(0)[0]

    current_version_title = generate_changelog_title(current_version)
    next_version_title = generate_changelog_title(next_version)

    next_release_template = f"{next_version_title}\n\n**unreleased**\n\n"

    changes = ""
    with builtins.open(changelog) as fd:
        changes += fd.read()

    changes = changes.replace(
        current_version_title, next_release_template + current_version_title
    )

    with builtins.open(changelog, "w") as fd:
        fd.write(changes)

    # Tries to load the EDITOR environment variable, else falls back to vim
    editor = os.environ.get("EDITOR", "vim")
    os.system(f"{editor} {changelog}")

    # Have to add it so it will be part of the commit
    subprocess.check_output(["git", "add", changelog])
    subprocess.check_output(["git", "commit", "-m", f"Changelog for {next_version}"])

    # Really run bumpver to set the new release and tag
    bv_args = ["bump-my-version", "bump", "--no-tag", "--new-version", next_version]

    subprocess.check_output(bv_args)


def main():
    """Parse command-line arguments and execute bumpversion command."""

    parser = ArgumentParser(prog="bumpversion", description="Bumpversion wrapper")

    default_changelog = os.path.join(os.getcwd(), "CHANGES.rst")

    subparsers = parser.add_subparsers(title="bumpversion wrapper commands")
    # release command
    release_doc = bump_release_version.__doc__
    subparser = subparsers.add_parser(
        "release", description=release_doc, formatter_class=RawTextHelpFormatter
    )
    subparser.add_argument(
        "--changelog",
        help="Project changelog",
        type=FileType(),
        default=default_changelog,
    )
    subparser.set_defaults(func=bump_release_version)
    # newversion command
    newversion_doc = bump_new_version.__doc__
    subparser = subparsers.add_parser(
        "newversion", description=newversion_doc, formatter_class=RawTextHelpFormatter
    )
    subparser.add_argument(
        "--changelog",
        help="Project changelog",
        type=FileType(),
        default=default_changelog,
    )
    subparser.add_argument(
        "part",
        help="Part of the version to be bumped",
        choices=["patch", "minor", "major"],
    )
    subparser.set_defaults(func=bump_new_version)
    # Parse argv arguments
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

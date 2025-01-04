# SPDX-FileCopyrightText: 2025-present kleines Filmröllchen <kleines@filmroellchen.eu>
#
# SPDX-License-Identifier: MIT
import click

from autotranscode.__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name=".")
def autotranscode():
    click.echo("Hello world!")

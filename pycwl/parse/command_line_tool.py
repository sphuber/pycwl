# -*- coding: utf-8 -*-
"""Module with methods to parse a document containing the specification of a command line tool."""
import io
import typing as t

import pydantic
import yaml

from pycwl.exceptions import DocumentParseError, SchemaValidationError
from pycwl.schema import CommandLineTool


def parse_command_line_tool(document: t.Union[t.TextIO, str]) -> CommandLineTool:
    """Parse a ``CommandLineTool`` document.

    :param document: document defining the command line tool.
    :raises :class:`pycwl.DocumentParseError`: if the YAML could not be parsed.
    :raises :class:`pycwl.SchemaValidationError`: if the command line tool invalides the schema.
    """
    if isinstance(document, str):
        document = io.StringIO(document)

    try:
        data = yaml.safe_load(document)
    except Exception as exception:
        raise DocumentParseError(f'Failed to parse the YAML document: {exception}') from exception

    try:
        return CommandLineTool(**data)
    except pydantic.ValidationError as exception:
        raise SchemaValidationError(
            f'The document does not respect the ``CommandLineTool`` schema: {exception}'
        ) from exception

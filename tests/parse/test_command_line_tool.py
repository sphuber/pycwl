# -*- coding: utf-8 -*-
"""Tests for the :mod:`pycwl.parse.command_line_tool` module."""
import typing

import pytest

from pycwl.exceptions import DocumentParseError, SchemaValidationError
from pycwl.parse.command_line_tool import parse_command_line_tool
from pycwl.schema import CommandLineTool


@pytest.mark.parametrize(
    'tool', (
        'base.cwl',
        'base_command_arguments.cwl',
        'base_command_list.cwl',
        'base_command_string.cwl',
        'inputs.cwl',
        'outputs.cwl',
    )
)
def test_parse_command_line_tool(data_regression, filepath_command_line_tool, tool):
    """Test the :meth:`pycwl.parse.command_line_tool.parse_command_line_tool` method."""
    with filepath_command_line_tool(tool).open() as handle:
        command_line_tool = parse_command_line_tool(handle)

    assert isinstance(command_line_tool, CommandLineTool)
    data_regression.check(command_line_tool.dict())


@pytest.mark.parametrize('document_type', (str, typing.IO))
def test_parse_command_line_tool_document_type(filepath_command_line_tool, document_type):
    """Test the :meth:`pycwl.parse.command_line_tool.parse_command_line_tool` method for varying ``document`` type."""
    document = filepath_command_line_tool('base.cwl')

    if document_type is str:
        command_line_tool = parse_command_line_tool(document.read_text())
    else:
        with document.open() as handle:
            command_line_tool = parse_command_line_tool(handle)

    assert isinstance(command_line_tool, CommandLineTool)


@pytest.mark.parametrize(
    'document, exception', (
        ('!!None', DocumentParseError),
        ('class: CommandLineTool', SchemaValidationError),
    )
)
def test_parse_command_line_tool_excepts(document, exception):
    """Test the :meth:`pycwl.parse.command_line_tool.parse_command_line_tool` method when it excepts."""
    with pytest.raises(exception):
        parse_command_line_tool(document)

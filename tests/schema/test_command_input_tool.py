# -*- coding: utf-8 -*-
"""Tests for the :mod:`pycwl.schema.command_line_tool` module."""
import pytest

from pycwl.schema.command_input_parameter import INPUT_PARAMETER_TYPE_MAP, InputParameterType
from pycwl.schema.command_line_tool import CommandLineTool


# yapf: disable
@pytest.mark.parametrize(
    'tool, expected', (
        (CommandLineTool(**{'inputs': [], 'outputs': []}), None),
        (CommandLineTool(**{'inputs': [], 'outputs': [], 'baseCommand': []}), None),
        (CommandLineTool(**{'inputs': [], 'outputs': [], 'baseCommand': ['command']}), 'command'),
        (CommandLineTool(**{'inputs': [], 'outputs': [], 'baseCommand': ['command', 'argument']}), 'command'),
    )
)
# yapf: enable
def test_command(tool, expected):
    """Test the :meth:`pycwl.schema.command_line_tool.CommandLineTool.command` property."""
    assert tool.command == expected


# yapf: disable
@pytest.mark.parametrize(
    'tool, expected', (
        (CommandLineTool(**{'inputs': [], 'outputs': []}), []),
        (CommandLineTool(**{'inputs': [], 'outputs': [], 'baseCommand': []}), []),
        (CommandLineTool(**{'inputs': [], 'outputs': [], 'baseCommand': ['command']}), []),
        (CommandLineTool(**{'inputs': [], 'outputs': [], 'baseCommand': ['command', 'argument']}), ['argument']),
        (CommandLineTool(**{'inputs': [], 'outputs': [], 'baseCommand': ['command', '-a', '-b']}), ['-a', '-b']),
    )
)
# yapf: enable
def test_base_arguments(tool, expected):
    """Test the :meth:`pycwl.schema.command_line_tool.CommandLineTool.base_arguments` property."""
    assert tool.base_arguments == expected


def test_validate_inputs():
    """Test the :meth:`pycwl.schema.command_line_tool.CommandLineTool.validate_inputs` validator."""
    inputs = [{'type': InputParameterType.BOOLEAN.value}]
    tool = CommandLineTool(inputs=inputs, outputs=[])
    assert isinstance(tool.inputs, list)
    assert isinstance(tool.inputs[0], INPUT_PARAMETER_TYPE_MAP[InputParameterType.BOOLEAN])

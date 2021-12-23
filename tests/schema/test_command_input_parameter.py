# -*- coding: utf-8 -*-
"""Tests for the :mod:`pycwl.schema.command_input_parameter` module."""
import pytest

from pycwl.schema.command_input_parameter import INPUT_PARAMETER_TYPE_MAP, CommandInputParameter, CommandLineBinding
from pycwl.schema.command_input_parameter import InputParameterType as T


@pytest.fixture
def parametrize_command_input_parameters(request):
    """Dynamic fixture returning instances ``CommandInputParameter`` based on the request typ.

    :param request: The parametrized request whose ``param`` attribute is expected to be a tuple of:

        * The ``InputParameterType`` for which to construct a parameter instance.
        * A dictionary that is passed as keyword arguments to the ``CommandInputParameter`` constructor.
        * A dictionary that is passed as keyword arguments to the ``CommandLineBinding`` constructor.
        * The value that is supposed to be passed to ``format_arguments``.
        * The expected return value of ``format_arguments``.
    """
    cls = INPUT_PARAMETER_TYPE_MAP[request.param[0]]
    input_binding = CommandLineBinding(**request.param[2])
    parameter = cls(type=request.param[0].value, **request.param[1], inputBinding=input_binding)
    return (parameter, *request.param[3:])


# yapf: disable
@pytest.mark.parametrize(
    'parametrize_command_input_parameters', (
        (T.BOOLEAN, {}, dict(prefix='--flag'), True, ['--flag']),
        (T.BOOLEAN, {}, dict(prefix='--flag'), False, []),
        (T.INT, {}, dict(prefix='--flag', separate=True), 42, ['--flag', '42']),
        (T.INT, {}, dict(prefix='--flag', separate=False), 42, ['--flag=42']),
        (T.FLOAT, {}, dict(prefix='--flag', separate=True), 12.3, ['--flag', '12.3']),
        (T.FLOAT, {}, dict(prefix='--flag', separate=False), 12.3, ['--flag=12.3']),
        (T.STRING, {}, dict(prefix='--flag', separate=True), 'shark', ['--flag', 'shark']),
        (T.STRING, {}, dict(prefix='--flag', separate=False), 'shark', ['--flag=shark']),
        (T.FILE, {'id': 'input_file'}, dict(prefix='--flag', separate=True), 'file.txt', ['--flag', '{input_file}']),
        (T.FILE, {'id': 'input_file'}, dict(prefix='--flag', separate=False), 'file.txt', ['--flag={input_file}']),
    ),
    indirect=True
)
# yapf: enable
def test_format_arguments(parametrize_command_input_parameters):
    """Test the :meth:`pycwl.schema.command_input_parameter.CommandInputParameter.format_arguments` method."""
    parameter, value, expected = parametrize_command_input_parameters
    assert parameter.format_arguments(value) == expected


def test_validate_binding():
    """Test the :meth:`pycwl.schema.command_input_parameter.CommandInputParameter.validate_binding` validator."""
    parameter = CommandInputParameter(type=T.BOOLEAN.value)
    assert isinstance(parameter.binding, CommandLineBinding)

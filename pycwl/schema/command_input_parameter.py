# -*- coding: utf-8 -*-
"""Schema definition of ``CommandInputParameter``."""
import enum
import pathlib
import typing as t

from pydantic import BaseModel, Field, validator

Expression = t.TypeVar('expression')

__all__ = (
    'CommandInputParameter', 'BoolCommandInputParameter', 'FileCommandInputParameter', 'FloatCommandInputParameter',
    'IntCommandInputParameter', 'StringCommandInputParameter', 'InputParameterType', 'INPUT_PARAMETER_TYPE_MAP'
)


class CommandLineBinding(BaseModel):
    """Schema definition of ``CommandLineBinding``."""

    position: int = 0
    prefix: str = None
    separate: bool = True
    item_separator: str = Field(None, alias='itemSeparator')
    value_from: t.Union[str, Expression] = Field(None, alias='valueFrom')
    shell_quote: bool = Field(True, alias='shellQuote')


class CommandInputParameter(BaseModel):
    """Schema definition of ``CommandInputParameter``."""

    type: str
    label: str = None
    identifier: str = Field(None, alias='id')
    streamable: bool = False
    binding: CommandLineBinding = Field(None, alias='inputBinding')
    default: t.Any = None
    doc: t.Union[str, t.List[str]] = None

    @validator('binding', pre=True, always=True)
    def validate_binding(cls, value):  # pylint: disable=no-self-argument,no-self-use
        """Validate and convert the ``binding`` field."""
        if value is None:
            return CommandLineBinding()

        return value

    def format_arguments(self, value) -> t.List[str]:
        """Format the input parameter into a list of command line arguments."""
        if self.binding.prefix is None:
            return [str(value)]

        if self.binding.separate:
            return [self.binding.prefix, str(value)]

        return [f'{self.binding.prefix}={value}']


class BoolCommandInputParameter(CommandInputParameter):
    """Data model for input parameters with type ``bool``."""

    def format_arguments(self, value) -> t.List[str]:
        """Format the input parameter into a list of command line arguments."""
        return [self.binding.prefix] if value else []


class FileCommandInputParameter(CommandInputParameter):
    """Data model for input parameters with type ``File``."""

    def format_file_binding(self, value) -> t.Dict[str, pathlib.Path]:
        """Format the input parameter's file bindings."""
        return {self.identifier: pathlib.Path(value['path']).resolve()}

    def format_arguments(self, value) -> t.List[str]:
        """Format the input parameter into a list of command line arguments."""
        if self.binding.prefix is None:
            return [f'{{{self.identifier}}}']

        if self.binding.separate:
            return [self.binding.prefix, f'{{{self.identifier}}}']

        return [f'{self.binding.prefix}={{{self.identifier}}}']


class FloatCommandInputParameter(CommandInputParameter):
    """Data model for input parameters with type ``float``."""


class IntCommandInputParameter(CommandInputParameter):
    """Data model for input parameters with type ``int``."""


class StringCommandInputParameter(CommandInputParameter):
    """Data model for input parameters with type ``str``."""


class InputParameterType(enum.Enum):
    """Enumeration of existing types of command input parameters."""

    NULL = 'null'
    BOOLEAN = 'boolean'
    INT = 'int'
    LONG = 'long'
    FLOAT = 'float'
    DOUBLE = 'double'
    STRING = 'string'
    FILE = 'File'


INPUT_PARAMETER_TYPE_MAP = {
    InputParameterType.NULL: CommandInputParameter,
    InputParameterType.BOOLEAN: BoolCommandInputParameter,
    InputParameterType.INT: IntCommandInputParameter,
    InputParameterType.LONG: IntCommandInputParameter,
    InputParameterType.FLOAT: FloatCommandInputParameter,
    InputParameterType.DOUBLE: FloatCommandInputParameter,
    InputParameterType.STRING: StringCommandInputParameter,
    InputParameterType.FILE: FileCommandInputParameter,
}

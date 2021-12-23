# -*- coding: utf-8 -*-
"""Schema definition of ``CommandOutputParameter``."""
import enum
import typing as t

from pydantic import BaseModel, Field

__all__ = (
    'CommandOutputParameter', 'FileCommandOutputParameter', 'StderrCommandOutputParameter',
    'StdoutCommandOutputParameter', 'OutputParameterType', 'OUTPUT_PARAMETER_TYPE_MAP'
)


class CommandOutputBinding(BaseModel):
    """Schema definition of ``CommandOutputBinding``."""

    glob: str = None
    load_contents: bool = Field(True, alias='loadContents')


class CommandOutputParameter(BaseModel):
    """Schema definition of ``CommandOutputParameter``."""

    type: str
    label: str = None
    identifier: str = Field(None, alias='id')
    streamable: bool = False
    binding: t.Optional[CommandOutputBinding] = Field(None, alias='outputBinding')
    doc: t.Union[str, t.List[str]] = None


class FileCommandOutputParameter(CommandOutputParameter):
    """Schema definition of ``FileCommandOutputParameter``."""


class StderrCommandOutputParameter(CommandOutputParameter):
    """Schema definition of ``StderrCommandOutputParameter``."""


class StdoutCommandOutputParameter(CommandOutputParameter):
    """Schema definition of ``StdoutCommandOutputParameter``."""


class OutputParameterType(enum.Enum):
    """Enumeration of existing types of command output parameters."""

    FILE = 'File'
    STDERR = 'stderr'
    STDOUT = 'stdout'


OUTPUT_PARAMETER_TYPE_MAP = {
    OutputParameterType.FILE: FileCommandOutputParameter,
    OutputParameterType.STDERR: StderrCommandOutputParameter,
    OutputParameterType.STDOUT: StdoutCommandOutputParameter,
}

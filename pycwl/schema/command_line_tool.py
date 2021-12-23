# -*- coding: utf-8 -*-
"""Schema definition of ``CommandLineTool``."""
import typing as t

from pydantic import BaseModel, Field, validator

from .command_input_parameter import INPUT_PARAMETER_TYPE_MAP, CommandInputParameter, InputParameterType
from .command_output_parameter import OUTPUT_PARAMETER_TYPE_MAP, CommandOutputParameter, OutputParameterType

__all__ = ('CommandLineTool',)


class CommandLineTool(BaseModel):
    """Schema definition of ``CommandLineTool``."""

    cls: str = Field('CommandLineTool', alias='class')
    cwl_version: str = Field(None, alias='cwlVersion')
    inputs: t.Union[t.List[CommandInputParameter], t.Dict[str, CommandInputParameter]]
    outputs: t.Union[t.List[CommandOutputParameter], t.Dict[str, CommandOutputParameter]]
    base_command: t.Union[str, t.List[str]] = Field(None, alias='baseCommand')

    @validator('inputs', pre=True)
    def validate_inputs(cls, value):  # pylint: disable=no-self-argument,no-self-use
        """Validate and convert the ``inputs`` field.

        The ``inputs`` can be specified as a list or a mapping. For consistency, in the case of a mapping, the value is
        converted to a list, where the keys are used to define the ``identifier`` field. The subclass that is used to
        create each ``CommandInputParameter`` is based on the ``type`` field of the input.
        """
        inputs = []

        if isinstance(value, dict):
            for identifier, data in value.items():
                parameter_type = InputParameterType(data['type'])
                parameter = INPUT_PARAMETER_TYPE_MAP[parameter_type](**data)
                parameter.identifier = identifier
                inputs.append(parameter)
        else:
            for data in value:
                parameter_type = InputParameterType(data['type'])
                parameter = INPUT_PARAMETER_TYPE_MAP[parameter_type](**data)
                inputs.append(parameter)

        return inputs

    @validator('outputs', pre=True)
    def validate_outputs(cls, value):  # pylint: disable=no-self-argument,no-self-use
        """Validate and convert the ``outputs`` field.

        The ``inputs`` can be specified as a list or a mapping. For consistency, in the case of a mapping, the value is
        converted to a list, where the keys are used to define the ``identifier`` field. The subclass that is used to
        create each ``CommandInputParameter`` is based on the ``type`` field of the input.
        """
        outputs = []

        if isinstance(value, dict):
            for identifier, data in value.items():
                parameter_type = OutputParameterType(data['type'])
                parameter = OUTPUT_PARAMETER_TYPE_MAP[parameter_type](**data)
                parameter.identifier = identifier
                outputs.append(parameter)
        else:
            for data in value:
                parameter_type = OutputParameterType(data['type'])
                parameter = OUTPUT_PARAMETER_TYPE_MAP[parameter_type](**data)
                outputs.append(parameter)

        return outputs

    @property
    def command(self) -> t.Optional[str]:
        """Return the command that should be executed.

        This corresponds to the first element of the ``baseCommand`` field if it is specified as a list, or else the
        command itself if specified directly.
        """
        if self.base_command is None:
            return None

        if isinstance(self.base_command, str):
            return self.base_command

        try:
            return self.base_command[0]
        except IndexError:
            return None

    @property
    def base_arguments(self) -> t.List[str]:
        """Return the base arguments that are to be used for the command.

        These correspond to the additional elements, besides the command itself, specified by the ``baseCommand`` field.
        If no base arguments are specified, the property returns an empty list.
        """
        if self.base_command is None:
            return []

        if isinstance(self.base_command, str):
            return []

        return self.base_command[1:]

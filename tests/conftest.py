# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,unused-argument
"""Configuration and fixtures for unit test suite."""
import pathlib

import pytest


@pytest.fixture
def filepath_fixtures() -> pathlib.Path:
    """Return the absolute filepath to the directory containing the file `fixtures`.

    :return: path to directory containing test fixture data.
    """
    return pathlib.Path(__file__).resolve().parent / 'fixtures'


@pytest.fixture
def filepath_command_line_tool(filepath_fixtures):
    """Return a factory to construct the path to the requested command line tool definition file."""

    def _factory(tool) -> pathlib.Path:
        """Return the path to the requested command line tool definition file."""
        return filepath_fixtures / 'documents' / 'command_line_tool' / tool

    return _factory

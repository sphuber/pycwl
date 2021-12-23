# -*- coding: utf-8 -*-
"""Module with custom exceptions."""

__all__ = ('DocumentParseError', 'SchemaValidationError')


class DocumentParseError(ValueError):
    """Raised when a CWL document contains invalid YAML and cannot be parsed."""


class SchemaValidationError(ValueError):
    """Raised when a CWL object is constructed from data that does not respect the schema."""

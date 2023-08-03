# Copyright (c) 2023 ANSYS, Inc. All rights reserved
"""Module for JSON validation purposes."""
import json
import os
from typing import List

from jsonschema import ValidationError, validate


def validate_output(output: List, schema_path: str = None):
    """Validate the output from the LLM with the given schema.

    Parameters
    ----------
    output : list
        Formatted output from LLM results.
    schema_path : str, optional.
        JSON schema file path to validate against. By default, ``None``,
        which falls back to the implemented schema inside the package.

    Returns
    -------
    bool

    """
    if schema_path is None:
        schema_path = os.path.join(
            os.path.dirname(__file__), "resources", "schema.json"
        )

    f = open(schema_path)
    schema = json.loads(f.read())
    try:
        validate(instance=output, schema=schema)
        return True
    except ValidationError:
        return False

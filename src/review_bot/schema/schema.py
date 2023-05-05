"""Module for JSON validation purposes."""
import json
import os
from typing import List

from jsonschema import validate


def validate_output(output: List, schema_path: str = None):
    """Validate the output from the LLM with the given schema.

    Parameters
    ----------
    output : List
        Formatted output from LLM results.
    schema_path : str, optional.
        JSON schema file path to validate against. By default, ``None``,
        which falls back to the implemented schema inside the package.
    """
    if schema_path is None:
        schema_path = os.path.join(
            os.path.dirname(__file__), "resources", "schema.json"
        )

    f = open(schema_path)
    schema = json.loads(f.read())
    validate(instance=output, schema=schema)

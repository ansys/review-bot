"""Module for JSON validation purposes."""
import json
import os
from typing import List

from jsonschema import validate


def validate_output(output: List, schema_path: str = "resources/schema.json"):
    """Validate the output from the LLM with the given schema.

    Parameters
    ----------
    output : List
        Formatted output from LLM results.
    schema_path : str
        JSON schema file path to validate against.
    """
    schema_rel_path = os.path.join(os.path.dirname(__file__), schema_path)

    f = open(schema_rel_path)
    schema = json.loads(f.read())
    validate(instance=output, schema=schema)

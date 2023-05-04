"""Miscellaneous functions."""

import json
import logging
import os
import re
from typing import Dict, List

from jsonschema import validate
import openai

LOG = logging.getLogger(__name__)
LOG.setLevel("DEBUG")


def _get_gh_token():
    """Return the github access token from the GITHUB_TOKEN environment variable."""
    access_token = os.environ.get("GITHUB_TOKEN")
    if access_token is None:
        raise OSError('Missing "GITHUB_TOKEN" environment variable')
    return access_token


def _set_open_ai_token():
    """Return the github access token from the GITHUB_TOKEN environment variable."""
    access_token = os.environ.get("OPEN_AI_TOKEN")
    if access_token is None:
        raise OSError('Missing "OPEN_AI_TOKEN" environment variable')
    openai.api_key = access_token


def open_logger(loglevel="DEBUG", formatstr="%(name)-20s - %(levelname)-8s - %(message)s"):
    """Start logging to standard output.

    Parameters
    ----------
    loglevel : str, optional
        Standard logging level. One of the following:

        - ``"DEBUG"`` (default)
        - ``"INFO"``
        - ``"WARNING"``
        - ``"ERROR"``
        - ``"CRITICAL"``

    formatstr : str, optional
        Format string.  See :class:`logging.Formatter`.

    Returns
    -------
    logging.RootLogger
        Root logging object.

    Examples
    --------
    Output logging to stdout at the ``'INFO'`` level.

    >>> import review_bot
    >>> review_bot.open_logger('INFO')

    """
    # don't add another handler if log has already been initialized
    if hasattr(open_logger, "log"):
        open_logger.log.handlers[0].setLevel(loglevel.upper())
    else:
        log = logging.getLogger()
        ch = logging.StreamHandler()
        ch.setLevel(loglevel.upper())

        ch.setFormatter(logging.Formatter(formatstr))
        log.addHandler(ch)
        open_logger.log = log

    return open_logger.log


def add_line_numbers(patch):
    """
    Add line numbers to the added lines in a given patch string.

    The function takes a patch string and adds line numbers to the lines that
    start with a '+'. It returns a new patch string with added line numbers.
    Line numbers are added immediately to the left of any '+'.

    Parameters
    ----------
    patch : str
        The patch string containing the changes in the file.

    Returns
    -------
    str
        The modified patch string with line numbers added to the added lines.

    Examples
    --------
    >>> patch = '''@@ -1,3 +1,5 @@
    ... +from itertools import permutations
    ... +
    ... import numpy as np
    ... import pytest'''
    >>> add_line_numbers(patch)
    '@@ -1,3 +1,5 @@
    1   +from itertools import permutations
    ... +
    ... import numpy as np
    ... import pytest'

    """
    lines = patch.splitlines()
    output_lines = []
    current_line = 0

    for line in lines:
        if line.startswith("@@ "):
            # Extract the new range (one with the +)
            new_range = int(line.split("+")[1].split(",")[0])

            # Update the current line number
            current_line = new_range
            output_lines.append(line)
        else:
            if line.startswith("+"):
                output_lines.append(f"{current_line: <5}{line}")
            else:
                output_lines.append(line)

            # Increment line number only if not starting with '-'
            if not line.startswith("-"):
                current_line += 1

    return "\n".join(output_lines)


def validate_output(output: List, schema_path: str):
    """_summary_

    Parameters
    ----------
    output : List
        Formatted output from LLM results.
    schema_path : str
        JSON schema file path to validate against.
    """
    f = open(schema_path)
    schema = json.loads(f.read())
    validate(instance=output, schema=schema)


def parse_suggestions(text_block: str) -> List[Dict[str, str]]:
    """Parse a given text block containing suggestions.

    Returns a list of dictionaries with keys: filename, lines, type, and text.

    Parameters
    ----------
    text_block : str
        The text block containing suggestions.

    Returns
    -------
    list of dict
        A list of dictionaries containing information about each suggestion.

    Examples
    --------
    >>> tblock = '''
    ... [tests/test_geometric_objects.py], [259-260], [SUGGESTION]: Replace `Rectangle` with `Quadrilateral` for clarity and consistency with the name of the class being tested.
    ... '''
    >>> parse_suggestions(tblock)
    [{'filename': 'tests/test_geometric_objects.py', 'lines': '259-260', 'type': 'SUGGESTION', 'text': 'Replace `Rectangle` with `Quadrilateral` for clarity and consistency with the name of the class being tested.'}]
    """
    LOG.debug("Parsing %s", text_block)
    suggestions = []
    pattern = r"\[(.*?)\], \[(.*?)\], \[(.*?)\]: (.*?)(?=\n\n\[|\n$)"
    matches = re.finditer(pattern, text_block, re.MULTILINE | re.DOTALL)

    for match in matches:
        suggestion = {
            "filename": match.group(1),
            "lines": match.group(2),
            "type": match.group(3),
            "text": match.group(4),
        }
        suggestions.append(suggestion)
    validate_output(
        output=suggestions,
        schema_path="schema.json",
    )
    return suggestions

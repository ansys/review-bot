"""Default variables for the project."""

import os

ACCESS_TOKEN = os.environ.get("OPEN_AI_TOKEN", None)
"""Default OpenAI token to use.

Get the OpenAI token from the environment variables.
"""

API_BASE = os.environ.get("OPENAI_API_BASE", None)
"""Default URL for OpenAI Azure API.

Get the URL of the OpenAI Azure service from the
environment variables.

"""
API_TYPE = os.environ.get("OPENAI_API_TYPE", None)
"""Default OpenAI API type.

Get the type of OpenAI API we are using from the
environment variables.
"""


API_VERSION = os.environ.get("OPENAI_API_VERSION", "2023-05-15")
"""Default OpenAI API Azure version we are using.

Get the OpenAI API Azure version from the environment variables.
You can check available versions in this link:
https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference#rest-api-versioning

"""

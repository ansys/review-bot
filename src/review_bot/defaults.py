"""Default variables for the project."""

import os

ACCESS_TOKEN = os.environ.get("OPEN_AI_TOKEN", None)
API_BASE = os.environ.get("OPENAI_API_BASE", None)
API_TYPE = os.environ.get("OPENAI_API_TYPE", None)
API_VERSION = os.environ.get("OPENAI_API_VERSION", "2023-05-15")

# Copyright (c) 2023 ANSYS, Inc. All rights reserved
"""OpenAI LLM powered Review-bot."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from .misc import open_logger
from .open_ai_interface import review_patch, review_patch_local

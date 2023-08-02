"""Test GitHub interface.

90% of this was written using chat gpt with the following prompt:

> Make this a pytest compatible test, and make it just a function test, do not make it a class.

"""
import os

import pytest

from review.bot.gh_interface import get_changed_files_and_contents

# Should be this repository
OWNER = "ansys-internal"
REPO = "review-bot"


def test_get_changed_files_and_contents():
    pull_number = 4

    files = get_changed_files_and_contents(OWNER, REPO, pull_number)

    assert isinstance(files, list)
    assert len(files) > 0
    assert isinstance(files[0], dict)
    assert "filename" in files[0]
    assert "status" in files[0]
    assert "file_text" in files[0]


def test_get_changed_files_and_contents_with_input_token():
    pull_number = 4

    access_token = os.environ.get("GITHUB_TOKEN")
    files = get_changed_files_and_contents(OWNER, REPO, pull_number, access_token)

    assert isinstance(files, list)
    assert len(files) > 0
    assert isinstance(files[0], dict)
    assert "filename" in files[0]
    assert "status" in files[0]
    assert "file_text" in files[0]


def test_get_changed_files_and_contents_raises_runtime_error():
    pull_number = 999999  # this is an issue

    with pytest.raises(RuntimeError):
        get_changed_files_and_contents(OWNER, REPO, pull_number)

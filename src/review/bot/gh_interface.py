# Copyright (c) 2023 ANSYS, Inc. All rights reserved
"""Contains functions to interface with GitHub."""
import logging
import threading

import requests

from review.bot.misc import _get_gh_token

LOG = logging.getLogger(__name__)
LOG.setLevel("DEBUG")


def _fetch_file_content(file_data, headers):
    """Fetch the content of a single file."""
    content_response = requests.get(
        file_data["contents_url"], headers=headers, timeout=10
    )

    if content_response.status_code == 200:
        content = content_response.json()
        file_data["file_text"] = requests.get(content["download_url"], timeout=10).text
    else:
        raise RuntimeError("Error fetching file content")


def get_changed_files_and_contents(owner, repo, pull_number, gh_access_token=None):
    r"""Retrieve the filenames, status, and contents of files changed in a GitHub PR.

    Parameters
    ----------
    owner : str
        The owner of the repository where the pull request was made.
    repo : str
        The name of the repository where the pull request was made.
    pull_number : int
        The number of the pull request to retrieve the changed files for.
    gh_access_token : str, optional
        GitHub token needed to communicate with the repository. By default, ``None``,
        which means it will try to read an existing env variable named ``GITHUB_TOKEN``.

    Returns
    -------
    list[dict]
        A list of dictionaries, where each dictionary represents a file that
        was changed in the pull request. The dictionary contains the following
        keys:

        - filename: str, the name of the file
        - status: str, the status of the file change ('added', 'modified', or 'removed')
        - file_text: str, the contents of the file as a string

    Raises
    ------
    RuntimeError
        If an error occurs while fetching the file content.

    Notes
    -----
    This function uses the GitHub API to retrieve the list of changed files in
    a pull request, along with the contents of each changed file. It requires a
    GitHub access token with appropriate permissions to access the repository.

    Example
    -------
    >>> files = get_changed_files_and_contents('my-org', 'my-repo', 123)
    >>> print(files[0]['filename'])
    'path/to/my-file.py'
    >>> print(files[0]['status'])
    'modified'
    >>> print(files[0]['file_text'])
    'print("Hello, world!")\n'

    """
    access_token = _get_gh_token() if gh_access_token is None else gh_access_token
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"
    # url = f"https://github.com/{owner}/{repo}/pull/{pull_number}.diff"
    headers = {
        "Authorization": f"Bearer {access_token}",
        # "Content-type": "application/vnd.github.diff",
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(
            f"Error fetching pull request files from:\n{url}\n\n{response.status_code}"
        )

    files = response.json()

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"Error fetching pull request files: {response.status_code}")
        return

    files = response.json()
    threads = []

    for file_data in files:
        LOG.info("Filename: %s", file_data["filename"])
        LOG.info("Status: %s", file_data["status"])

        thread = threading.Thread(target=_fetch_file_content, args=(file_data, headers))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return files

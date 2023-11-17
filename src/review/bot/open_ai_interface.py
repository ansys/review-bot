# Copyright (c) 2023 ANSYS, Inc. All rights reserved
"""Functions to interface with OpenAI."""
import logging
from typing import Dict, List

import review.bot.defaults as defaults
from review.bot.exceptions import EmptyOpenAIResponseException
from review.bot.gh_interface import get_changed_files_and_contents
from review.bot.git_interface import LocalGit
from review.bot.misc import add_line_numbers, get_client, parse_suggestions

LOG = logging.getLogger(__name__)
LOG.setLevel("DEBUG")

# Developer note:
# There is a significant improvement in the completion using gpt-4 vs gpt-3.5-turbo
OPEN_AI_MODEL = defaults.API_MODEL


def review_patch(
    owner: str,
    repo: str,
    pr: int,
    use_src: bool = False,
    filter_filename=None,
    gh_access_token: str = None,
    docs_only: bool = False,
    config_file: str = None,
) -> List[Dict]:
    """Review a patch in a pull request and generate suggestions for improvement.

    Parameters
    ----------
    owner : str
        The GitHub owner/organization of the repository.
    repo : str
        The name of the repository on GitHub.
    pr : str
        The pull request number.
    use_src : bool, default: False
        Use the source file as context for the patch. Works for small files and
        not for large ones.
    filter_filename : str, optional
        If set, filters out all but the file matching this string.
    gh_access_token : str, optional
        GitHub token needed to communicate with the repository. By default, ``None``,
        which means it will try to read an existing env variable named ``GITHUB_TOKEN``.
    config_file : str, optional
        Path to OpenAI configuration file. By default, ``None``.
    Returns
    -------
    list[dict]
        A dictionary containing suggestions for the reviewed patch.
    """
    # Fetch changed files and contents
    changed_files = get_changed_files_and_contents(owner, repo, pr, gh_access_token=gh_access_token)
    # assemble suggestions
    suggestions = []
    n_hits = 0
    for file_data in changed_files:
        filename = file_data["filename"]
        if filter_filename is not None and filename != filter_filename:
            LOG.debug("Skipping %s due to filter_filename = %s", filename, filter_filename)
            continue

        patch = add_line_numbers(file_data["patch"])
        if docs_only:
            file_src = f"FILENAME: {filename}\nCONTENT:\n{file_data['file_text']}"
            suggestions.extend(
                generate_suggestions(filename, file_src, patch, config_file, docs_only=True)
            )
        elif use_src:
            file_src = f"FILENAME: {filename}\nCONTENT:\n{file_data['file_text']}"
            suggestions.extend(generate_suggestions(filename, file_src, patch, config_file))
        else:
            suggestions.extend(generate_suggestions(filename, patch))
        n_hits += 1

    if filter_filename is not None and n_hits < 1:
        raise ValueError(f"No files matching '{filter_filename}'")

    return suggestions


def review_folder(
    owner: str,
    repo: str,
    pr: int,
    folder: str,
    gh_access_token: str = None,
    config_file: str = None,
) -> List[Dict]:
    """Reviews an specific file from the PR. The file must have been modified in the PR.

    Parameters
    ----------
    owner : str
        The GitHub owner/organization of the repository.
    repo : str
        The name of the repository on GitHub.
    pr : str
        The pull request number.
    folder : str
        Name of the folder you want to review.
    gh_access_token : str, optional
        GitHub token needed to communicate with the repository. By default, ``None``,
        which means it will try to read an existing env variable named ``GITHUB_TOKEN``.
    config_file : str, optional
        Path to OpenAI configuration file. By default, ``None``.

    Returns
    -------
    List[Dict]
        List of dictionaries with the PR suggestions.
    """
    # Fetch changed files and contents
    changed_files = get_changed_files_and_contents(owner, repo, pr, gh_access_token=gh_access_token)
    # assemble suggestions
    suggestions = []
    for file_data in changed_files:
        filename = file_data["filename"]
        if folder in filename:
            file_src = f"FILENAME: {filename}\nCONTENT:\n{file_data['file_text']}"
            suggestions.extend(generate_suggestions(filename, file_src, config_file))
    return suggestions


def review_file(
    owner: str,
    repo: str,
    pr: int,
    filename: str,
    gh_access_token: str = None,
    config_file: str = None,
) -> List[Dict]:
    """Reviews an specific file from the PR. The file must have been modified in the PR.

    Parameters
    ----------
    owner : str
        The GitHub owner/organization of the repository.
    repo : str
        The name of the repository on GitHub.
    pr : str
        The pull request number.
    filename : str
        Name of the file you want to review.
    gh_access_token : str, optional
        GitHub token needed to communicate with the repository. By default, ``None``,
        which means it will try to read an existing env variable named ``GITHUB_TOKEN``.
    config_file : str, optional
        Path to OpenAI configuration file. By default, ``None``.

    Returns
    -------
    List[Dict]
        List of dictionaries with the PR suggestions.
    """
    # Fetch changed files and contents
    changed_files = get_changed_files_and_contents(owner, repo, pr, gh_access_token=gh_access_token)
    # assemble suggestions
    suggestions = []
    for file_data in changed_files:
        if filename in file_data["filename"]:
            print(file_data["filename"])
            file_src = f"FILENAME: {filename}\nCONTENT:\n{file_data['file_text']}"
            suggestions.extend(generate_suggestions(filename, file_src, config_file))
            break
    return suggestions


def review_patch_local(
    repo: str,
    branch: str = None,
    use_src: bool = False,
    filter_filename: str = None,
    config_file: str = None,
) -> List[Dict]:
    """Review a patch in a pull request and generate suggestions for improvement.

    Parameters
    ----------
    repo : str
        The path to the local repository.
    branch : str
        Name of the branch you want to compare to main. By default, current branch.
    use_src : bool, default: False
        Use the source file as context for the patch. Works for small files and
        not for large ones.
    filter_filename : str, optional
        If set, filters out all but the file matching this string.
    config_file : str, optional
        Path to OpenAI configuration file. By default, ``None``.

    Returns
    -------
    list[dict]
        A dictionary containing suggestions for the reviewed patch.
    """
    # load repo and change branch if it applies
    local_repo = LocalGit(repo)
    if branch is not None:
        local_repo.change_branch(branch_name=branch)

    # Fetch changed files and contents
    changed_files = local_repo.get_local_patch()
    file_sources = local_repo.get_file_sources()
    # assemble suggestions
    suggestions = []
    n_hits = 0
    for filename, patch in changed_files.items():
        if filter_filename is not None and filename != filter_filename:
            LOG.debug("Skipping %s due to filter_filename = %s", filename, filter_filename)
            continue

        if use_src:
            file_src = f"FILENAME: {filename}\nCONTENT:\n{file_sources['file_text']}"
            suggestions.extend(generate_suggestions(filename, file_src, patch, config_file))
        else:
            suggestions.extend(generate_suggestions(filename, patch))
        n_hits += 1

    if filter_filename is not None and n_hits < 1:
        raise ValueError(f"No files matching '{filter_filename}'")

    return suggestions


def message_generation(
    filename: str, patch: str = None, file_src: str = None, docs_only: bool = False
) -> str:
    """Generate the required message for each type of query request.

    Parameters
    ----------
    filename : str
        Name of the file being patched.
    patch : str
        The patch text containing line numbers and changes.
    file_src : str
        The source file text including the file name and its contents.
    docs_only: True
        Flag to select whether to review the documentation only or not.

    Returns
    -------
    list[dict]
        A list with the messages to send to the LLM.
    """
    messages = []
    if file_src and patch:
        messages = [
            {
                "role": "system",
                "content": """
You are a GitHub review bot.  You first expect the full source of the file to be reviewed followed by the patch which contains the line number. You respond after the full source file with 'Ready for the patch.'. After the patch, you provide 'review items' to improve just the patch code using the context from the full source file. Do not include the line numbers in any code suggestions. There are 3 TYPEs of review items [GLOBAL, SUGGESTION, INFO]. Each review item must be in the format [<FILENAME>], [<LINE-START>(-<LINE-END>)], [TYPE]: <Review text>

Type: GLOBAL
This must always included. This is a general overview of the file patch. If the file looks good, simply respond with "No issues found, LGTM!". Otherwise, indicate the kind of comments and suggestions that will be given in the files tab. Make this section short and do not include any line numbers (i.e., leave [<LINE-START>(-<LINE-END>)] empty.

Type: SUGGESTION
This is where code must be changed or should be changed. If you are replacing code, it must use the GitHub markdown code block with ```suggestion, and the [<LINE-START>-<LINE-END>] must match the line(s) that will be replaced. If you are adding new code, you should only include the [<LINE-START>] where you expect the code to be inserted. Do not insert code that is outside of the patch.

Type: INFO
This is for comments that do not include code that you want to replace. These should be logical errors, style suggestions, or other issues with the code. You can feel free to include example code, and if you do use markdown formatting, but this is primarily for text comments.
""",
            },
            {"role": "user", "content": file_src},
            {"role": "assistant", "content": "Ready for the patch."},
            {
                "role": "user",
                "content": f"{patch}\n\nReview the above code patch and provide recommendations for improvement or point out errors.",
            },
        ]
    elif docs_only and file_src:
        messages = [
            {
                "role": "system",
                "content": """
You are a GitHub review bot.  You expect the full source of the file to be reviewed. There are 2 TYPEs of review items [GLOBAL, SUGGESTION]. Each review item must be in the format [<FILENAME>], [<LINE-START>(-<LINE-END>)], [TYPE]: <Review text>

You are a technical writer and grammar expert.
You want to improve docstrings in your Python client library.
You want docstrings in the numpydoc format.
You want complete sentences, with verbs in the present tense.
You never want to combine sentences.
You want to use double backticks to surround the names of classes, functions, methods, parameters, parameter options, attributes, and data objects.
You want to use Oxford commas and omit articles from the beginning of descriptions for parameters, attributes, properties, and return values.
You want to capitalize only proper nouns.


Type: GLOBAL
This must always included. This is a general overview of the file patch. If the file looks good, simply respond with "No issues found, LGTM!". Otherwise, indicate the kind of comments and suggestions that will be given in the files tab. Make this section short and do not include any line numbers (i.e., leave [<LINE-START>(-<LINE-END>)] empty.

Type: SUGGESTION
This is where code must be changed or should be changed. This should only contain docstrings or docstring modifications. If you are replacing code, it must use the GitHub markdown code block with ```suggestion, and the [<LINE-START>-<LINE-END>] must match the line(s) that will be replaced. If you are adding new code, you should only include the [<LINE-START>] where you expect the code to be inserted. Do not insert code that is outside of the patch.

            """,
            },
            {"role": "user", "content": file_src},
            {"role": "assistant", "content": "Ready for the doc review."},
            {
                "role": "user",
                "content": f"""Improve this module, adding numpydoc docstrings where missing.
End all descriptions with a period. Keep sentences short and simple. Omit unnecessary commas.
For method and function descriptions, start the docstring with a simple verb (no "s" or "es" at the end of the verb).
For class descriptions, start the docstring with a verb ending in an "s" or "es".
Place names of classes, methods, parameters, data objects, and commands in double backticks (``).
Follow code in backticks with the noun describing whether this code represents (such as a method, function, parameter, or command).
When specifying a default parameter value, use the format "The default is ..., in which case the ...." Place the default value in double backticks.
When the default value is "None", format it as ``None``.
Instead of "used to" before a verb, replace with "for" and the gerund form of the verb.
Instead of "to be" before a verb ending in "ed", replace with "to" and the simple verb form (without the "ed".
For a boolean parameter, start the description with "Whether ..."
For a boolean return value, use the description "``True`` when successful, ``False`` when failed."
For property descriptions, use only a noun string followed by a period.
Replace the Latin phrase "e.g." with "for example" and the Latin phrase "i.e." with "that is". Begin a new sentence with "For example,". Do not include as part of the previous sentence.
Replace "Retrieve", "Obtain", "Find", and "Return" with "Get".
Spell ANSYS as Ansys, hfss as HFSS, edb as EDB, boolean as Boolean.
Provide a summary of the changes that are made.""",
            },
        ]
    elif file_src and not patch:
        messages = [
            {
                "role": "system",
                "content": """
You are a GitHub review bot.  You first expect full filename. You then expect a patch from a GitHub pull request and you provide 'review items' to improve just the patch code using the context from the full source file. Do not include the line numbers in any code suggestions. There are 3 TYPEs of review items [GLOBAL, SUGGESTION, COMMENT]. Each review item must be in the format [<FILENAME>], [<LINE-START>(-<LINE-END>)], [TYPE], always between brackets: <Review text>

Type: GLOBAL
This must always be included. This is a general overview of the file patch. If the file looks good, simply respond with "No issues found, LGTM!". Otherwise, indicate the kind of comments and suggestions that follow. Make this section short and do not include any line numbers (i.e., leave [<LINE-START>(-<LINE-END>)] empty.

Type: SUGGESTION
This is where code must be changed or should be changed. If you are replacing code, it must use the GitHub markdown code block with ```suggestion, and the [<LINE-START>-<LINE-END>] must match the line(s) that will be replaced. If you are adding new code, you should only include the [<LINE-START>] where you expect the code to be inserted. Do not insert code that is outside of the patch.

Type: COMMENT
This is for comments that do not include code that you want to replace. These should be logical errors, style suggestions, or other issues with the code. You can feel free to include example code, and if you do use markdown formatting, but this is primarily for text comments.
""",
            },
            {"role": "user", "content": filename},
            {"role": "assistant", "content": "Ready for the patch."},
            {
                "role": "user",
                "content": f"{file_src}\n\nReview the above code file source and provide recommendations for improvement or point out errors.",
            },
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": """
You are a GitHub review bot.  You first expect full filename. You then expect a patch from a GitHub pull request and you provide 'review items' to improve just the patch code using the context from the full source file. Do not include the line numbers in any code suggestions. There are 3 TYPEs of review items [GLOBAL, SUGGESTION, COMMENT]. Each review item must be in the format [<FILENAME>], [<LINE-START>(-<LINE-END>)], [TYPE], always between brackets: <Review text>

Type: GLOBAL
This must always included. This is a general overview of the file patch. If the file looks good, simply respond with "No issues found, LGTM!". Otherwise, indicate the kind of comments and suggestions that follow. Make this section short and do not include any line numbers (i.e., leave [<LINE-START>(-<LINE-END>)] empty.

Type: SUGGESTION
This is where code must be changed or should be changed. If you are replacing code, it must use the GitHub markdown code block with ```suggestion, and the [<LINE-START>-<LINE-END>] must match the line(s) that will be replaced. If you are adding new code, you should only include the [<LINE-START>] where you expect the code to be inserted. Do not insert code that is outside of the patch.

Type: COMMENT
This is for comments that do not include code that you want to replace. These should be logical errors, style suggestions, or other issues with the code. You can feel free to include example code, and if you do use markdown formatting, but this is primarily for text comments.
""",
            },
            {"role": "user", "content": filename},
            {"role": "assistant", "content": "Ready for the patch."},
            {
                "role": "user",
                "content": f"{patch}\n\nReview the above code patch and provide recommendations for improvement or point out errors.",
            },
        ]
    return messages


def generate_suggestions(
    filename, patch=None, file_src=None, config_file: str = None, docs_only=False
) -> List[Dict[str, str]]:
    """
    Generate suggestions for a given file source and patch.

    Parameters
    ----------
    filename : str
        Name of the file being patched.
    patch : str, optional
        The patch text containing line numbers and changes.
    file_src: str, optional
        Source file of the patch.
    config_file : str, optional
        Path to OpenAI configuration file. By default, ``None``.
    docs_only: bool, optional
        Whether to review documentation only or the whole code. By default ``False``.
    Returns
    -------
    list[dict]
        A list of dictionaries containing suggestions for the patch.
    """
    client = get_client(config_file)
    LOG.debug("Generating suggestions for a given file source and patch.")
    LOG.debug("FILENAME: %s", filename)
    LOG.debug("PATCH: %s", patch)
    messages = message_generation(
        patch=patch, filename=filename, file_src=file_src, docs_only=docs_only
    )

    response = client.chat.completions.create(model=OPEN_AI_MODEL, messages=messages)
    LOG.debug(response)
    # Extract suggestions
    text = response.choices[0].message.content
    if len(text) == 0:
        raise EmptyOpenAIResponseException()
    return parse_suggestions(text)

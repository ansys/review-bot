"""Functions to interface with OpenAI."""
from enum import Enum
import logging
from typing import Dict, List

import openai

from review_bot.exceptions import EmptyOpenAIResponseException
from review_bot.gh_interface import get_changed_files_and_contents
from review_bot.git_interface import LocalGit
from review_bot.hf_model import Inference
from review_bot.misc import _set_open_ai_config, add_line_numbers, parse_suggestions


class InferenceMotor(Enum):
    """Enum for the types of inference motors available."""

    OPENAI = 0
    HUGGINGFACE = 1


LOG = logging.getLogger(__name__)
LOG.setLevel("DEBUG")

# Developer note:
# There is a significant improvement in the completion using gpt-4 vs gpt-3.5-turbo
OPEN_AI_MODEL = "gpt-4"


def hf_prompt_patch(filename: str, patch: str) -> str:
    """Generate the prompt for HF patch review.

    Parameters
    ----------
    filename : str
        Name of the file to review.
    patch : str
        Diff patch to review

    Returns
    -------
    str
        Prompt result.
    """
    prompt = f"""
You are a GitHub review bot.  You first expect full filename. You then expect a patch from a GitHub pull request and you provide 'review items' to improve just the patch code using the context from the full source file. Do not include the line numbers in any code suggestions. There are 3 TYPEs of review items [GLOBAL, SUGGESTION, COMMENT]. Each review item must be in the format [<FILENAME>], [<LINE-START>(-<LINE-END>)], [TYPE], always between brackets: <Review text>

Type: GLOBAL
This must always included. This is a general overview of the file patch. If the file looks good, simply respond with "No issues found, LGTM!". Otherwise, indicate the kind of comments and suggestions that follow. Make this section short and do not include any line numbers (i.e., leave [<LINE-START>(-<LINE-END>)] empty.

Type: SUGGESTION
This is where code must be changed or should be changed. If you are replacing code, it must use the GitHub markdown code block with ```suggestion, and the [<LINE-START>-<LINE-END>] must match the line(s) that will be replaced. If you are adding new code, you should only include the [<LINE-START>] where you expect the code to be inserted. Do not insert code that is outside of the patch.

Type: COMMENT
This is for comments that do not include code that you want to replace. These should be logical errors, style suggestions, or other issues with the code. You can feel free to include example code, and if you do use markdown formatting, but this is primarily for text comments.

Filename: {filename}

Source:
{patch}\n\nReview the above code patch and provide recommendations for improvement or point out errors."
"""

    return prompt


def hf_prompt_source(source: str, patch: str) -> str:
    """Generate the prompt for HF patch review with source.

    Parameters
    ----------
    source : str
        Source of the file to review.
    patch : str
        Diff patch to review

    Returns
    -------
    str
        Prompt result.
    """
    prompt = f"""
You are a GitHub review bot.  You first expect the full source of the file to be reviewed followed by the patch which contains the line number. You respond after the full source file with 'Ready for the patch.'. After the patch, you provide 'review items' to improve just the patch code using the context from the full source file. Do not include the line numbers in any code suggestions. There are 3 TYPEs of review items [GLOBAL, SUGGESTION, INFO]. Each review item must be in the format [<FILENAME>], [<LINE-START>(-<LINE-END>)], [TYPE]: <Review text>

Type: GLOBAL
This must always included. This is a general overview of the file patch. If the file looks good, simply respond with "No issues found, LGTM!". Otherwise, indicate the kind of comments and suggestions that will be given in the files tab. Make this section short and do not include any line numbers (i.e., leave [<LINE-START>(-<LINE-END>)] empty.

Type: SUGGESTION
This is where code must be changed or should be changed. If you are replacing code, it must use the GitHub markdown code block with ```suggestion, and the [<LINE-START>-<LINE-END>] must match the line(s) that will be replaced. If you are adding new code, you should only include the [<LINE-START>] where you expect the code to be inserted. Do not insert code that is outside of the patch.

Type: INFO
This is for comments that do not include code that you want to replace. These should be logical errors, style suggestions, or other issues with the code. You can feel free to include example code, and if you do use markdown formatting, but this is primarily for text comments.

Source:

{source}

Patch:

{patch}

\n\nReview the above code patch and provide recommendations for improvement or point out errors.

"""
    return prompt


def openai_prompt_patch(filename: str, patch: str) -> List:
    """Generate the prompt for OpenAI patch review.

    Parameters
    ----------
    source : str
        Source of the file to review.
    patch : str
        Diff patch to review

    Returns
    -------
    List
        List with the required format for OpenAI.
    """
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


def openai_prompt_source(source: str, patch: str) -> List:
    """Generate the prompt for OpenAI patch review with the source code.

    Parameters
    ----------
    source : str
        Source of the file to review.
    patch : str
        Diff patch to review

    Returns
    -------
    List
        List with the required format for OpenAI.
    """
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
        {"role": "user", "content": source},
        {"role": "assistant", "content": "Ready for the patch."},
        {
            "role": "user",
            "content": f"{patch}\n\nReview the above code patch and provide recommendations for improvement or point out errors.",
        },
    ]
    return messages


def review_patch(
    owner, repo, pr, use_src=False, filter_filename=None, gh_access_token=None
):
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

    Returns
    -------
    list[dict]
        A dictionary containing suggestions for the reviewed patch.
    """
    # Fetch changed files and contents
    changed_files = get_changed_files_and_contents(
        owner, repo, pr, gh_access_token=gh_access_token
    )
    # assemble suggestions
    suggestions = []
    n_hits = 0
    for file_data in changed_files:
        filename = file_data["filename"]
        if filter_filename is not None and filename != filter_filename:
            LOG.debug(
                "Skipping %s due to filter_filename = %s", filename, filter_filename
            )
            continue

        patch = add_line_numbers(file_data["patch"])
        if use_src:
            file_src = f"FILENAME: {filename}\nCONTENT:\n{file_data['file_text']}"
            suggestions.extend(
                generate_suggestions_with_source(filename, file_src, patch)
            )
        else:
            suggestions.extend(generate_suggestions(filename, patch))
        n_hits += 1

    if filter_filename is not None and n_hits < 1:
        raise ValueError(f"No files matching '{filter_filename}'")

    return suggestions


def review_patch_local(
    repo: str, branch: str = None, use_src=False, filter_filename=None
):
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
            LOG.debug(
                "Skipping %s due to filter_filename = %s", filename, filter_filename
            )
            continue

        if use_src:
            file_src = f"FILENAME: {filename}\nCONTENT:\n{file_sources['file_text']}"
            suggestions.extend(
                generate_suggestions_with_source(filename, file_src, patch)
            )
        else:
            suggestions.extend(generate_suggestions(filename, patch))
        n_hits += 1

    if filter_filename is not None and n_hits < 1:
        raise ValueError(f"No files matching '{filter_filename}'")

    return suggestions


def generate_suggestions_with_source(
    filename: str,
    file_src: str,
    patch: str,
    inference_motor: InferenceMotor = InferenceMotor.OPENAI,
) -> List[Dict[str, str]]:
    """Generate suggestions for a given file source and patch.

    Parameters
    ----------
    filename : str
        Name of the file being patched.
    file_src : str
        The source file text including the file name and its contents.
    patch : str
        The patch text containing line numbers and changes.
    inference_motor : InferenceMotor
        Which inference motor you want to use, by default OPENAI.

    Returns
    -------
    list[dict]
        A list of dictionaries containing suggestions for the patch.
    """
    _set_open_ai_config()
    LOG.debug("Generating suggestions for a given file source and patch.")
    LOG.debug("FILENAME: %s", filename)
    LOG.debug("PATCH: %s", patch)

    if inference_motor == InferenceMotor.OPENAI:
        response = openai.ChatCompletion.create(
            model=OPEN_AI_MODEL, messages=openai_prompt_source(file_src, patch)
        )
        text = response["choices"][0].message.content

    elif inference_motor == InferenceMotor.HUGGINGFACE:
        model = Inference()
        text = model.evaluate(instruction=hf_prompt_source(file_src, patch))
    # Extract suggestions
    if len(text) == 0:
        raise EmptyOpenAIResponseException()
    return parse_suggestions(text)


def generate_suggestions(
    filename, patch, inference_motor: InferenceMotor = InferenceMotor.OPENAI
) -> List[Dict[str, str]]:
    """
    Generate suggestions for a given file source and patch.

    Parameters
    ----------
    filename : str
        Name of the file being patched.
    patch : str
        The patch text containing line numbers and changes.

    Returns
    -------
    list[dict]
        A list of dictionaries containing suggestions for the patch.
    """
    _set_open_ai_config()
    LOG.debug("Generating suggestions for a given file source and patch.")
    LOG.debug("FILENAME: %s", filename)
    LOG.debug("PATCH: %s", patch)

    if inference_motor == InferenceMotor.OPENAI:
        response = openai.ChatCompletion.create(
            model=OPEN_AI_MODEL, messages=openai_prompt_patch(filename, patch)
        )
        text = response["choices"][0].message.content

    elif inference_motor == InferenceMotor.HUGGINGFACE:
        model = Inference()
        text = model.evaluate(instruction=hf_prompt_patch(filename, patch))
    # Extract suggestions
    if len(text) == 0:
        raise EmptyOpenAIResponseException()
    return parse_suggestions(text)

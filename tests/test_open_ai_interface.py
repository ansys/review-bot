import warnings

import pytest

from review.bot import review_patch

# Should be this repository
OWNER = "ansys"
REPO = "review-bot"


@pytest.mark.flaky(retries=3, delay=5)
def test_patch_cpp():
    # no matching files
    with pytest.raises(ValueError, match="No files matching"):
        _ = review_patch(
            OWNER,
            REPO,
            2,
            use_src=False,
            filter_filename="tests/samples/cplus/function.cpp",
        )

    sugg = review_patch(
        OWNER,
        REPO,
        4,
        use_src=False,
        filter_filename="tests/samples/cplus/function.cpp",
    )
    assert isinstance(sugg, list)
    if len(sugg) < 1:
        warnings.warn(
            "No suggestions provided by OpenAI. Global should at least be included",
            UserWarning,
        )
        return

    if not any(sug["type"] == "GLOBAL" for sug in sugg):
        warnings.warn("GLOBAL info should at least be included", UserWarning)

    assert isinstance(sugg[0], dict)
    words = " ".join([sug["text"] for sug in sugg])
    search_word = "pointer"
    if search_word not in words.lower():
        warnings.warn(f"the word '{search_word}' not in suggestions", UserWarning)


@pytest.mark.flaky(retries=3, delay=5)
def test_patch_python():
    sugg = review_patch(
        OWNER,
        REPO,
        4,
        use_src=True,
        filter_filename="tests/samples/py/functions.py",
        docs_only=True,
    )

    assert isinstance(sugg, list)
    if len(sugg) < 1:
        warnings.warn(
            "No suggestions provided by OpenAI. Global should at least be included",
            UserWarning,
        )
        return

    if not any(sug["type"] == "GLOBAL" for sug in sugg):
        warnings.warn("GLOBAL info should at least be included", UserWarning)

    assert isinstance(sugg[0], dict)
    words = " ".join([sug["text"] for sug in sugg])
    search_word = "mutable"
    if search_word not in words.lower():
        warnings.warn(f"the word '{search_word}' not in suggestions", UserWarning)


@pytest.mark.flaky(retries=3, delay=5)
def test_docs_python():
    sugg = review_patch(
        OWNER,
        REPO,
        4,
        use_src=True,
        filter_filename="tests/samples/py/functions_no_docs.py",
        docs_only=True,
    )

    assert isinstance(sugg, list)
    if len(sugg) < 1:
        warnings.warn(
            "No suggestions provided by OpenAI. Global should at least be included",
            UserWarning,
        )
        return

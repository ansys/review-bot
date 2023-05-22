"""Module for CLI related code."""

import argparse
import os

from review_bot import review_patch_local


def show_review(args):
    """
    Show through command line the review of the diff from the LLM.

    Parameters
    ----------
    args
        Args from the command line.
    """
    repo_path = args.review[0]
    if ".git" not in os.listdir(repo_path):
        raise Exception("Not a git repository.")
    sugg = review_patch_local(repo_path)
    for suggestion in sugg:
        text = f"""
        -> In file {os.path.join(repo_path, suggestion["filename"])}, in lines {suggestion["lines"]}:

        {suggestion["text"]}

        """
        print(text)


def main():
    """Entrypoint to execute."""
    parser = argparse.ArgumentParser(description="Reviewbot CLI")

    parser.add_argument(
        "-r",
        "--review",
        type=str,
        nargs=1,
        help="Review the diff of the local repo you selected",
    )

    args = parser.parse_args()
    if args.review != None:
        show_review(args)


if __name__ == "__main__":
    main()

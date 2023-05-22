"""Interface module for local GIT files."""
import os
from pathlib import Path

from git import Repo


class LocalGit:
    """Class to extract information from a diff in a local repository.

    Parameters
    ----------
    repo_path : str
        Path to the local repository.
    """

    def __init__(self, repo_path: str):
        """Receives the path to the local repo."""
        self._repo = Repo(repo_path)
        self._repo_path = repo_path

    def _preprocess_patch(self):
        """Clean the string returned by the diff of many unwanted lines.

        Returns
        -------
        list
            Diff without unnecessary lines and separated by file.
        """
        # get the repo and get the diff of the last commit with main
        tree = self._repo.heads.main.commit.tree
        diff = self._repo.git.diff(tree)

        # remove unwanted lines
        diff_lines = diff.split("\n")
        diff_lines_aux = []
        i = 0
        while i < len(diff_lines):
            if diff_lines[i].startswith("diff"):
                i += 3
            else:
                diff_lines_aux.append(diff_lines[i])
                i += 1

        # rejoin the diff into one single string
        diff_processed = "\n".join(diff_lines)
        diff_files = diff_processed.split("+++")

        # first element is always empty
        return diff_files[1:]

    def get_filenames(self):
        """Get the filenames of the diff files.

        Returns
        -------
        list
            List with the filenames.
        """
        diff_files = self._preprocess_patch()

        # get names of the files affected by the diff
        diff_filenames = []
        for file in diff_files:
            name = file.split("\n")[0][3:]
            if name != "":
                diff_filenames.append(name)
        return diff_filenames

    def get_local_patch(self):
        """Process the raw diff to extract the filename and useful info.

        Returns
        -------
        Dict
            Dict with the file name as key and the diff as content.
        """
        diff_files = self._preprocess_patch()
        diff_filenames = self.get_filenames()

        # associate filenames with the code changes
        patch_dict = {}
        for filename, file in zip(diff_filenames, diff_files):
            patch_dict[filename] = file
        return patch_dict

    def change_branch(self, branch_name: str):
        """Switch the branch of the repo to the required one.

        Parameters
        ----------
        branch_name : str
            Branch to switch to.
        """
        # TODO: Raise error if you have uncommitted changes
        git = self._repo.git
        git.checkout(branch_name)

    def get_file_sources(self):
        """Get the text from the code files of the diff.

        Returns
        -------
        Dict
            Dict with the file name as key and the source file as content.
        """
        file_sources = {}
        for filename in self.get_filenames():
            absolute_path = os.path.join(self._repo_path, filename)
            source = Path(absolute_path).read_text()
            file_sources[filename] = source
        return file_sources

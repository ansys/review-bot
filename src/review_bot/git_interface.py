"""Interface module for local GIT files."""
from git import Repo


class LocalDiff:
    """Class to extract information from a diff in a local repository.

    Parameters
    ----------
    repo_path : str
    Path to the local repository
    """

    def __init__(self, repo_path: str):
        """Receives the path to the local repo."""
        self.repo_path = repo_path
        self._patch = self.get_local_path()
        self._files = self._patch.keys()

    @property
    def patch(self):
        """Return dict with the file name as key and the diff as content.

        Returns
        -------
        Dict
            Dict with the file name as key and the diff as content.
        """
        return self._patch

    @property
    def files(self):
        """Names of the files.

        Returns
        -------
        List
            Names of the files.
        """
        return self._files

    def _get_local_patch(self):
        """Process the raw diff to extract the filename and useful info.

        Returns
        -------
        Dict
            Dict with the file name as key and the diff as content.
        """
        # TODO: refactor
        # get the repo and get the diff of the last commit with main
        repo = Repo(self.repo_path)
        tree = repo.heads.main.commit.tree
        diff = repo.git.diff(tree)

        # remove unwanted lines
        diff_lines = diff.split("\n")
        diff_lines_aux = []
        for i in range(len(diff_lines)):
            if diff_lines[i].startswith("diff"):
                for j in range(3):
                    diff_lines_aux.append(diff_lines[i + j])

        for line in diff_lines_aux:
            diff_lines.remove(line)

        # rejoin the diff into one single string
        diff_processed = "\n".join(diff_lines)
        diff_files = diff_processed.split("+++")

        # get names of the files affected by the diff
        diff_filenames = []
        for file in diff_files:
            name = file.split("\n")[0][3:]
            if name != "":
                diff_filenames.append(name)

        # associate filenames with the code changes
        patch_dict = {}
        for i in range(len(diff_filenames)):
            patch_dict[diff_filenames[i]] = diff_files[i]
        return patch_dict

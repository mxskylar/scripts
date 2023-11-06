import os

CONFIG_FILE = "config.yaml"


class GitRepoException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GitRepoClient:
    def __init__(self, repository_path):
        self.repository_path = repository_path
        git_installation = os.popen("which git").read().strip()
        git_repo_path = os.popen(f"cd {repository_path}; git rev-parse --show-toplevel").read().strip()
        self.is_valid_git_repo = git_installation and git_repo_path == repository_path

    def stage_recipe_files(self):
        """Returns staged recipe files with uncommitted changes"""
        uncommitted_files = self.__get_uncommitted_files__()
        if not uncommitted_files:
            raise GitRepoException(f"No files with uncommitted changes in {self.repository_path}")
        # Ignore the config file. Do not stage or return it. All the other files should be recipe files.
        os.popen(f"cd {self.repository_path}; git add . && git reset {CONFIG_FILE}")
        return [file_name for file_name in uncommitted_files if file_name != CONFIG_FILE]

    def __get_uncommitted_files__(self):
        git_status = os.popen(
            f"cd {self.repository_path}; "
            + "git status --short | "
            + "sed -e 's/A //g' -e 's/\?\? //g'"  # Strips symbols indicating whether a file is staged or not
        )
        # Strip quotes from file names and add them to a list split by each new line
        status_items = git_status.read().replace('"', '').split(os.linesep)
        uncommitted_files = []
        for item in status_items:
            file_name = item.strip()
            # Ignore empty strings in the status_items list
            if file_name:
                uncommitted_files.append(f"{self.repository_path}/{file_name}")
        return uncommitted_files


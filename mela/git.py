import os

CONFIG_FILE_NAME = "config.yaml"


class MelaGitException(Exception):
    def __init__(self, message):
        super().__init__(message)


def stage_recipe_files(recipes_dir):
    """Returns staged recipe files with uncommitted changes"""
    git_installation = os.popen("which git")
    if not git_installation.read():
        raise MelaGitException("Git is not installed")
    recipe_files = get_uncommitted_recipe_files(recipes_dir)
    if not recipe_files:
        raise MelaGitException(f"No new recipes imported into {recipes_dir}")
    os.popen(f"cd {recipes_dir}; git add . && git reset config.yaml")
    return recipe_files


def get_uncommitted_recipe_files(recipes_dir):
    git_status = os.popen(
        f"cd {recipes_dir}; "
        + "git status --short | "
        + f"grep -v 'config.yaml' | "  # Ignore config file, all other files should be recipes
        + "sed -e 's/A //g' -e 's/\?\? //g'"  # Strips symbols indicating whether a file is staged or not
    )
    # Strip quotes from file names and add them to a list split by each new line
    status_items = git_status.read().replace('"', '').split(os.linesep)
    recipe_files = []
    for item in status_items:
        recipe_file_name = item.strip()
        # Ignore empty strings in the status_items list
        if recipe_file_name:
            recipe_files.append(f"{recipes_dir}/{recipe_file_name}")
    return recipe_files

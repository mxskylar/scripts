import os


class RecipeFormatterGitException(Exception):
    def __init__(self, message):
        super().__init__(message)


def git_stage_recipe_files(recipes_dir):
    git_installation = os.popen("which git")
    if not git_installation.read():
        raise RecipeFormatterGitException("Git is not installed")
    git_status = os.popen(f"cd {recipes_dir}; git status --short | grep -v 'config.yaml'")
    if not git_status.read():
        raise RecipeFormatterGitException(f"No new recipes imported into {recipes_dir}")
    os.popen(f"cd {recipes_dir}; git add . && git reset config.yaml")


def format_recipes(recipes):
    print(recipes)

import json


class Recipe:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path) as file:
            # Mela JSON format for individually exported recipes: https://mela.recipes/fileformat/index.html
            self.json_object = json.loads(file.read())

    def format_recipe(self, format_config):
        """Formats recipe according to config and updates the recipe file"""
        # TODO: Format ingredient prefixes & suffixes
        # TODO: Remove WIP label/category if it exists for a recipe, after formatting it
        print(self.json_object)

    def __update_recipe_file__(self):
        # TODO Overwrite recipe file with JSON string
        print(self.file_path)

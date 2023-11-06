import json
import os
from mela.config import Config


class Recipe:
    def __init__(self, file_path, config: Config):
        self.config = config
        self.file_path = file_path
        with open(self.file_path) as file:
            # Mela JSON format for individually exported recipes: https://mela.recipes/fileformat/index.html
            self.json_object = json.loads(file.read())
            self.ingredients = [
                ingredient.strip() for ingredient in self.json_object['ingredients'].split(os.linesep)
                if not ingredient.strip().startswith('#')
            ]

    def format_recipe(self):
        """Formats recipe according to config and updates the recipe file"""
        # TODO: Format ingredient prefixes & suffixes
        # TODO: Remove WIP label/category if it exists for a recipe, after formatting it
        formatted_ingredients = []
        for ingredient in self.ingredients:
            for configured_ingredient in self.config.ingredients:
                preceding, prefix, ingredient, following = (
                    self.__get_ingredient__pieces__(ingredient, configured_ingredient)
                )
        print(self.file_path)

    @staticmethod
    def __get_ingredient__pieces__(ingredient, configured_ingredient):
        return ingredient, ingredient, ingredient, ingredient

    def __write_updated_json_object_to_file__(self):
        # TODO Overwrite recipe file with JSON string
        print(self.file_path)

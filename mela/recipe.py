import json
import os
import re

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
        print(self.file_path)
        prefixed_ingredients = []
        for ingredient in self.ingredients:
            ingredient_to_add = ingredient
            for configured_ingredient in self.config.ingredients:
                prefixed_ingredient = self.__get_maybe_prefixed_ingredient__(ingredient, configured_ingredient)
                if prefixed_ingredient:
                    ingredient_to_add = prefixed_ingredient
                    break
            prefixed_ingredients.append(ingredient_to_add)
        print(prefixed_ingredients)
        # TODO: Format ingredient suffixes
        # TODO: Remove WIP label/category if it exists for a recipe, after formatting it

    @staticmethod
    def __get_maybe_prefixed_ingredient__(ingredient, configured_ingredient):
        for name in configured_ingredient['names']:
            regex_match = re.search(f'(.*)((?i){name})(.*)', ingredient)
            if regex_match:
                regex_groups = regex_match.groups()
                last_3_chars = regex_groups[0][-3:]
                if (
                        last_3_chars.endswith(' ')
                        and last_3_chars[1] != ' '
                        and last_3_chars.startswith(' ')
                ):
                    return (
                            f"{regex_groups[0][:-3]} {configured_ingredient['prefix']} "
                            + f"{regex_groups[1]}{regex_groups[2]}"
                    )
                return (
                        f"{regex_groups[0].strip()} {configured_ingredient['prefix']} "
                        + f"{regex_groups[1]}{regex_groups[2]}"
                )
        return None

    def __write_updated_json_object_to_file__(self):
        # TODO Overwrite recipe file with JSON string
        print(self.file_path)

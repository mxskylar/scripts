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
            self.json_object['ingredients'] = [
                 ingredient.strip() for ingredient in self.json_object['ingredients'].split(os.linesep)
                if not ingredient.strip().startswith('#')
            ]

    def format_recipe(self):
        """Formats recipe according to config and updates the recipe file"""
        # Ingredients
        formatted_ingredients = []
        for ingredient in self.json_object['ingredients']:
            ingredient_to_add = ingredient
            for configured_ingredient in self.config.ingredients:
                ingredient_regex_match = self.__is_ingredient_match__(ingredient, configured_ingredient['names'])
                if ingredient_regex_match:
                    ingredient_regex_groups = ingredient_regex_match.groups()
                    ingredient_name = ingredient_regex_groups[1]
                    # Add prefixes, if any
                    prefixed_ingredient = self.__get_prefixed_ingredient__(
                        ingredient_regex_groups,
                        configured_ingredient['prefix']
                    )
                    ingredient_to_add = prefixed_ingredient if prefixed_ingredient else ingredient_to_add
                    # Add suffixes, if any
                    if 'suffix' in configured_ingredient.keys():
                        suffixed_ingredients = self.__get_suffixed_ingredient__(
                            ingredient_name,
                            ingredient_to_add,
                            configured_ingredient['suffix']
                        )
                        ingredient_to_add = suffixed_ingredients if suffixed_ingredients else ingredient_to_add
                    break
            formatted_ingredients.append(ingredient_to_add)
        self.json_object['ingredients'] = os.linesep.join(formatted_ingredients)

        # Categories - Remove WIP category if it exists
        categories_to_use = []
        for category in self.json_object['categories']:
            if category != "WIP":
                categories_to_use.append(category)
        self.json_object['categories'] = categories_to_use

        self.__write__to_file__()

    @staticmethod
    def __is_ingredient_match__(ingredient, configured_ingredient_names):
        for name in configured_ingredient_names:
            regex_match = re.search(f'(.*)((?i){name})(.*)', ingredient)
            if regex_match:
                return regex_match
        return False

    @staticmethod
    def __get_prefixed_ingredient__(regex_groups, prefix):
        last_3_chars = regex_groups[0][-3:]
        if (
                last_3_chars.endswith(' ')
                and last_3_chars[1] != ' '
                and last_3_chars.startswith(' ')
        ):
            return (
                    f"{regex_groups[0][:-3]} {prefix} "
                    + f"{regex_groups[1]}{regex_groups[2]}"
            )
        return (
                f"{regex_groups[0].strip()} {prefix} "
                + f"{regex_groups[1]}{regex_groups[2]}"
        )

    @staticmethod
    def __get_suffixed_ingredient__(ingredient_name, ingredient, suffix):
        regex_match = re.search(f'(.*)((?i){ingredient_name}.*)(\\(.*\\))', ingredient)
        if regex_match:
            regex_groups = regex_match.groups()
            return f"{regex_groups[0]}{regex_groups[1]} ({suffix.strip()})"
        return f"{ingredient.strip()} ({suffix.strip()})"

    def __write__to_file__(self):
        with open(self.file_path, "w") as file:
            file.write(json.dumps(self.json_object))

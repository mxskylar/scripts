import yaml

ALL_VALIDATORS = {
    'ingredients': lambda ingredients: validate_ingredients(ingredients)
}


class MissingConfigKeyException(Exception):
    """Exception raised when config is missing a required key"""
    def __init__(self, yaml_keys_string):
        super().__init__(f"Key {yaml_keys_string} missing from YAML config")


class InvalidConfigTypeException(Exception):
    """Exception raised when contents of config have an invalid type"""
    def __init__(self, yaml_keys_string, requirement_message):
        super().__init__(f"{yaml_keys_string} {requirement_message}")


def validate_ingredients(ingredients):
    if not type(ingredients) is list:
        return False, "must be a list"
    for ingredient in ingredients:
        if (
                not type(ingredient) is dict
                or len(ingredient.keys()) < 2
                or len(ingredient.keys()) > 3
        ):
            return False, "must be a map with 2 or 3 keys: 'names', 'prefix', & optional key 'suffix'"
        if (
                "names" not in ingredient.keys()
                or not type(ingredient['names']) is list
                or any(type(name) is not str for name in ingredient['names'])
        ):
            return False, "must contain key 'names' that is a list of strings"
        if (
                "prefix" not in ingredient.keys()
                or not type(ingredient['prefix']) is str
        ):
            return False, "must contain key 'prefix' that is a string"
        if len(ingredient.keys()) > 2 and (
                "suffix" not in ingredient.keys()
                or not type(ingredient['suffix'] is str)
        ):
            return False, "must be a map with 2 or 3 keys. Optional third key must be 'suffix', which must be a string."
    return True, ""


def validate(validators, content, parent_yaml_keys_string=""):
    for key, value in validators.items():
        yaml_keys_string = f"{parent_yaml_keys_string}.{key}" if parent_yaml_keys_string else key
        if callable(value):
            is_valid, error_message = value(content[key])
            if not is_valid:
                raise InvalidConfigTypeException(yaml_keys_string, error_message)
            return True
        else:
            if key not in content.keys():
                raise MissingConfigKeyException(yaml_keys_string)
            return validate(validators[key], content[key], yaml_keys_string)


class Config:
    def __init__(self, yaml_config_path):
        with open(yaml_config_path, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            validate(ALL_VALIDATORS, content)
            self.ingredients = content['ingredients']

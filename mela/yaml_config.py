import yaml

ALL_VALIDATORS = {
    'format': {
        'ingredients': {
            'prefixes': (
                lambda value:
                    type(value) is dict and all(type(item) is str and len(item) == 1 for item in value.values()),
                "must be map<string, string> with values that are one character long"
            )
            # TODO: Add validation rules for ingredient suffixes which will appear such as: ingredient (suffix)
        }
    }
}


class YamlConfigMissingKeyException(Exception):
    """Exception raised when YAML config is missing a required key"""
    def __init__(self, yaml_keys_string):
        super().__init__(f"Key {yaml_keys_string} missing from YAML config")


class YamlConfigInvalidTypeException(Exception):
    """Exception raised when contents of YAML config have an invalid type"""
    def __init__(self, yaml_keys_string, requirement_message):
        super().__init__(f"{yaml_keys_string} {requirement_message}")


def validate(validators, content, parent_yaml_keys_string=""):
    for key, value in validators.items():
        yaml_keys_string = f"{parent_yaml_keys_string}.{key}" if parent_yaml_keys_string else key
        if type(value) is tuple:
            is_valid, requirement_message = value
            if not is_valid(content[key]):
                raise YamlConfigInvalidTypeException(yaml_keys_string, requirement_message)
            return True
        else:
            if key not in content.keys():
                raise YamlConfigMissingKeyException(yaml_keys_string)
            return validate(validators[key], content[key], yaml_keys_string)


def get_config(config_path):
    with open(config_path, "r") as yaml_file:
        content = yaml.safe_load(yaml_file)
    validate(ALL_VALIDATORS, content)
    return content

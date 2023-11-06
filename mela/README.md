# Mela Recipe Formatter

Formats the ingredients in Mela recipe JSON files to have the prefix and/or suffix
specified in the `config.yaml` file in a given directory.

For example, the following prefixes & suffixes will be added to ingredients
with the following names if the prefixes & suffixes do not already exist in the ingredient:

```yaml
ingredients:
  - names:
      - sweet potato
      - sweet potatoes
    prefix: 🟡
  - names:
      - pasta # Refer to gluten-free alternatives as gluten-free "pasta" to avoid collisions
    prefix: 🟡
    suffix: "75 g / 3 oz / 1/2 cup per day"
```

To format the ingredients, run the following command,
which will format recipes in `$HOME/mela` by default:

```bash
mela format
```

To format ingredients in a different directory,
pass the directory to the command like so:

```bash
mela format --recipes /path/to/my/directory
```
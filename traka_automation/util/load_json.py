import json

WHITESPACE_TRANSLATION = str.maketrans(
    {
        "\u00a0": " ",
        "\u2007": " ",
        "\u202f": " ",
    }
)


def load_json(path):
    """Load a JSON file into a dictionary."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = text.translate(WHITESPACE_TRANSLATION)
    print(repr(text))
    return json.loads(text)

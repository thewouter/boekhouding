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
    return json.loads(text)


def write_json(path: str, data: dict):
    """Write a dictionary to a JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

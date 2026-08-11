import yaml

DEFAULT_SECRETS_FILE = "/onedrive/conf/secrets.yaml"


class Config:
    """Class to hold the configuration.

    It lazy loads the secrets file."""

    config: dict | None = None

    def __init__(self, secrets_file: str = DEFAULT_SECRETS_FILE):
        print("initializing config")
        self.secrets_file = secrets_file

    def __getitem__(self, item):
        """Get a value from the config."""
        if self.config is None:
            self.set_config(get_config(self.secrets_file))
        assert self.config is not None
        return self.config[item]

    def set_config(self, config: dict):
        self.config = config


def get_config(secrets_file: str):
    with open(secrets_file, "r") as f:
        return yaml.safe_load(f.read())


secrets_config = Config()

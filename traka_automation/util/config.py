import yaml


def get_config():
    with open("/onedrive/conf/secrets.yaml", "r") as f:
        return yaml.safe_load(f.read())


secrets_config = get_config()

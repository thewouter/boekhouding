from traka_automation.util.config import secrets_config


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print("xxxx")
    secrets_config.set_config(
        {
            "ms_graph": {
                "tenant_id": "your-tenant-id",
                "client_id": "your-client-id",
                "client_secret": "your-client-secret",
            },
            "mollie": {
                "api_key": "xxxxx",
            },
            "dev": True,
        }
    )

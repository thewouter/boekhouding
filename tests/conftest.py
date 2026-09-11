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
            "paynl": {
                "service_id": "SL-1234-1234",
                "secret": "xxxxx",
            },
            "dev": True,
            "email": {
                "mailbox": "inschrijvingen@trapperskamp.com",
                "signature_name": "Wouter van Harten",
                "signature_title": "Penningmeester Plusscoutkring Trapperskamp",
            },
        }
    )

import msal
import requests

from traka_automation.util.config import secrets_config

TENANT_ID = secrets_config["ms_graph"]["tenant_id"]
CLIENT_ID = secrets_config["ms_graph"]["client_id"]
CLIENT_SECRET = secrets_config["ms_graph"]["client_secret"]


def draft_email(mailbox: str, to_addresses: list[str], subject: str, body: str) -> None:
    """Draft an email_handler to the mailbox."""
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )

    token = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    access_token = token["access_token"]

    mail = {
        "subject": subject,
        "body": {"contentType": "HTML", "content": body},
        "toRecipients": [
            {"emailAddress": {"address": address}} for address in to_addresses
        ],
    }

    response = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{mailbox}/messages",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=mail,  # type: ignore[arg-type]
    )

    response.raise_for_status()

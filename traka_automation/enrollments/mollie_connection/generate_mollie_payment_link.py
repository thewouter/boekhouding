from datetime import datetime

from mollie.api.client import Client
from mollie.api.objects.payment_link import PaymentLink

from traka_automation.enrollments.mollie_connection.dummy_payment_link import (
    DummyPaymentLink,
)
from traka_automation.util.config import secrets_config


def get_mollie_client() -> Client:
    """Get a mollie_connection client."""
    mollie_key = secrets_config["mollie"]["api_key"]
    mollie_client = Client()
    mollie_client.set_api_key(mollie_key)
    return mollie_client


def generate_payment_link(
    name: str, camp: str, amount: float, end_date: datetime
) -> PaymentLink:
    """Get the payment link for the Enrollment through the Mollie API."""
    mollie_client = get_mollie_client()
    if secrets_config["dev"]:
        return DummyPaymentLink(client=mollie_client, data={})
    payment_link: PaymentLink = mollie_client.payment_links.create(
        {
            "description": f"Deelname van {name} aan {camp}.",
            "amount": {
                "currency": "EUR",
                "value": f"{amount:0.2f}",
            },
            "minimumAmount": None,
            "expiresAt": end_date.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "reusable": False,
            "allowedMethods": ["ideal"],
            "sequenceType": "oneoff",
        }
    )

    return payment_link

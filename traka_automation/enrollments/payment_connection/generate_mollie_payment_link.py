from datetime import datetime

from mollie.api.client import Client
from mollie.api.objects.payment_link import PaymentLink

from traka_automation.enrollments.models.payment_link import TrakaPaymentLink
from traka_automation.settings import MollieSettings


def get_mollie_client(settings: MollieSettings) -> Client:
    """Get a payment_connection client."""
    mollie_client = Client()
    mollie_client.set_api_key(settings.api_key)
    return mollie_client


def generate_mollie_payment_link(
    name: str,
    camp: str,
    amount: float,
    end_date: datetime,
    settings: MollieSettings,
) -> TrakaPaymentLink:
    """Get the payment link for the Enrollment through the Mollie API."""
    mollie_client = get_mollie_client(settings)
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

    return TrakaPaymentLink(
        payment_link=payment_link.payment_link,
        order_id=payment_link.id,
    )

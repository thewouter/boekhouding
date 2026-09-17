from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from traka_automation.enrollments.models.payment_link import TrakaPaymentLink
from traka_automation.settings import PayNlSettings

PAYNL_ORDER_URL = "https://connect.pay.nl/v1/orders"
IDEAL_PAYMENT_METHOD_ID = 10
REFERENCE_MAX_LENGTH = 32
RETURN_URL = "https://trapperskamp.com"


def _paynl_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _paynl_payload(
    name: str,
    camp_name: str,
    amount: float,
    end_date: datetime,
    quantity: int,
    settings: PayNlSettings,
) -> dict[str, object]:
    reference = (f"{camp_name[:20]}-{name[:20]}-{end_date:%Y%m%d}").replace(" ", "-")
    description = f"Deelname van {name} aan {camp_name}."
    unit_amount = round(amount * 100 / quantity)
    return {
        "serviceId": settings.service_id,
        "description": description,
        "reference": reference[:REFERENCE_MAX_LENGTH],
        "returnUrl": RETURN_URL,
        "amount": {
            "value": round(amount * 100),
            "currency": "EUR",
        },
        "order": {
            "products": [
                {
                    "description": camp_name,
                    "type": "ARTICLE",
                    "price": {
                        "value": unit_amount,
                        "currency": "EUR",
                    },
                    "quantity": quantity,
                }
            ]
        },
        "integration": {
            "pointOfInteraction": "PAYMENT_REQUEST"
        },
        "expire": end_date.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
    }


def generate_paynl_payment_link(
    name: str,
    camp_name: str,
    amount: float,
    end_date: datetime,
    quantity: int = 1,
    settings: PayNlSettings | None = None,
) -> TrakaPaymentLink:
    """Get the payment link for the Enrollment through the Pay.nl API."""
    if settings is None:
        raise ValueError("Pay.nl settings are required")
    response = requests.post(
        PAYNL_ORDER_URL,
        headers=_paynl_headers(),
        auth=HTTPBasicAuth(settings.service_id, settings.secret),
        json=_paynl_payload(name, camp_name, amount, end_date, quantity, settings),
        timeout=30,
    )
    response.raise_for_status()
    response_data = response.json()
    redirect_url = response_data["links"]["redirect"]
    return TrakaPaymentLink(payment_link=redirect_url, order_id=response_data.get("id"))

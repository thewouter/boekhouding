from datetime import datetime

from traka_automation.enrollments.models import DummyTrakaPaymentLink, TrakaPaymentLink
from traka_automation.enrollments.payment_connection.generate_mollie_payment_link import (
    generate_mollie_payment_link,
)
from traka_automation.enrollments.payment_connection.generate_paynl_payment_link import (
    generate_paynl_payment_link,
)
from traka_automation.util.config import secrets_config


def generate_payment_link(
    name: str,
    camp_name: str,
    amount: float,
    end_date: datetime,
    quantity: int = 1,
) -> TrakaPaymentLink:
    """Get the payment link for the Enrollment through the Pay.nl API."""
    if secrets_config["dev"]:
        return DummyTrakaPaymentLink()

    if secrets_config["payment_service_provider"] == "mollie":
        payment_link = generate_mollie_payment_link(name, camp_name, amount, end_date)
    elif secrets_config["payment_service_provider"] == "paynl":
        payment_link = generate_paynl_payment_link(
            name, camp_name, amount, end_date, quantity
        )
    else:
        raise ValueError(
            f"Unknown payment service provider: {secrets_config['payment_service_provider']}"
        )

    return TrakaPaymentLink(
        payment_link=payment_link.payment_link, order_id=payment_link.order_id
    )

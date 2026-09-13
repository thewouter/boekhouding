from datetime import datetime

from traka_automation.enrollments.models.enrollment_web_form import EnrollmentWebForm
from traka_automation.enrollments.models.payment_link import (
    DummyTrakaPaymentLink,
    TrakaPaymentLink,
)
from traka_automation.enrollments.payment_connection.generate_mollie_payment_link import (
    generate_mollie_payment_link,
)
from traka_automation.enrollments.payment_connection.generate_paynl_payment_link import (
    generate_paynl_payment_link,
)
from traka_automation.settings import AppSettings, PaymentServiceProvider


def generate_payment_link(
    name: str,
    camp_name: str,
    amount: float,
    end_date: datetime,
    settings: AppSettings,
    quantity: int = 1,
) -> TrakaPaymentLink:
    """Get the payment link for the Enrollment through the Pay.nl API."""
    if settings.dev:
        return DummyTrakaPaymentLink()

    if settings.payment_service_provider == PaymentServiceProvider.MOLLIE:
        if settings.mollie is None:
            raise ValueError("Mollie settings are required")
        payment_link = generate_mollie_payment_link(
            name, camp_name, amount, end_date, settings.mollie
        )
    elif settings.payment_service_provider == PaymentServiceProvider.PAYNL:
        if settings.paynl is None:
            raise ValueError("Pay.nl settings are required")
        payment_link = generate_paynl_payment_link(
            name, camp_name, amount, end_date, quantity, settings.paynl
        )
    else:
        raise ValueError(
            f"Unknown payment service provider: {settings.payment_service_provider}"
        )

    return TrakaPaymentLink(
        payment_link=payment_link.payment_link, order_id=payment_link.order_id
    )


def get_payment_link(
    enrollment: EnrollmentWebForm,
    settings: AppSettings,
) -> TrakaPaymentLink | None:
    """Get the payment link for the Enrollment."""
    if enrollment.camp.price is None:
        return None
    if enrollment.payment_link_cache is None:
        enrollment.payment_link_cache = generate_payment_link(
            name=enrollment.combined_names,
            camp_name=enrollment.camp.name,
            amount=enrollment.total_price,
            end_date=enrollment.camp.end_date,
            quantity=len(enrollment.participants),
            settings=settings,
        )
        if enrollment.payment_link_cache is None:
            raise ValueError("Payment link not available")
    return enrollment.payment_link_cache

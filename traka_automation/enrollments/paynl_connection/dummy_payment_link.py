from traka_automation.enrollments.paynl_connection.payment_link import PaymentLink


class DummyPaymentLink(PaymentLink):
    payment_link: str = "https://google.com"
    order_id: str | None = "dummy-order"

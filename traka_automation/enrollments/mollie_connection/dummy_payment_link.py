from mollie.api.objects.payment_link import PaymentLink


class DummyPaymentLink(PaymentLink):
    payment_link = "https://google.com"
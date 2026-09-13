from pydantic import BaseModel


class TrakaPaymentLink(BaseModel):
    payment_link: str
    order_id: str


class DummyTrakaPaymentLink(TrakaPaymentLink):
    payment_link: str = "https://google.com"
    order_id: str = "dummy-order"

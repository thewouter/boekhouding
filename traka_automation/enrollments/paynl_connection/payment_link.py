from pydantic import BaseModel


class PaymentLink(BaseModel):
    payment_link: str
    order_id: str | None = None

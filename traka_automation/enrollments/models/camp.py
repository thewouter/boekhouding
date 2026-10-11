import math
from datetime import datetime, timedelta

from pydantic import BaseModel

from traka_automation.util.dutch_date import dutch_date


class CancellationTerm(BaseModel):
    date: datetime
    retainer: float

    @property
    def text_date(self):
        return dutch_date(self.date)

    @property
    def text_retainer(self):
        return f"€{self.retainer:.2f}"


CANCELLATION_INTERVAL_ONE = timedelta(days=60)
CANCELLATION_INTERVAL_TWO = timedelta(days=30)


class Camp(BaseModel):
    """A camp that can be enrolled in."""

    name: str
    price: float | None
    start_date: datetime
    end_date: datetime

    @property
    def start_date_string(self):
        return dutch_date(self.start_date)

    @property
    def end_date_string(self):
        return dutch_date(self.end_date)

    @property
    def cancellation_term_one(self):
        return CancellationTerm(
            date=self.start_date - CANCELLATION_INTERVAL_ONE,
            retainer=self.price * 0.25 if self.price else 0,
        )

    @property
    def cancellation_term_two(self):
        return CancellationTerm(
            date=self.start_date - CANCELLATION_INTERVAL_TWO,
            retainer=self.price * 0.5 if self.price else 0,
        )

    @property
    def year(self):
        return self.start_date.year

    @property
    def allows_for_two_payment_terms(self):
        return "mission" in self.name.lower() or "trex" in self.name.lower()

    @property
    def payment_term_one(self) -> float:
        if self.price is None:
            raise ValueError("Camp has no price")
        term_one = math.ceil((self.price * 0.5) / 50) * 50
        return min(term_one, self.price)

    @property
    def payment_term_two(self) -> float:
        if self.price is None:
            raise ValueError("Camp has no price")
        return self.price - self.payment_term_one

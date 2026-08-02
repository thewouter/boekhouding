from datetime import datetime, timedelta

from pydantic import BaseModel
import locale

from traka_automation.util.dutch_date import dutch_date


class CancellationTerm(BaseModel):
    date: datetime
    retainer: float

    @property
    def text_date(self):
        return dutch_date(self.date)


CANCELLATION_INTERVAL_ONE = timedelta(days=60)
CANCELLATION_INTERVAL_TWO = timedelta(days=30)


class Camp(BaseModel):
    """A camp that can be enrolled in."""

    name: str
    price: float
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
            date=self.start_date - CANCELLATION_INTERVAL_ONE, retainer=self.price * 0.25
        )

    @property
    def cancellation_term_two(self):
        return CancellationTerm(
            date=self.start_date - CANCELLATION_INTERVAL_TWO, retainer=self.price * 0.5
        )

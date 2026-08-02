from datetime import datetime, timedelta

from pydantic import BaseModel
import locale


class CancellationTerm(BaseModel):
    date: datetime
    retainer: float


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
        locale.setlocale(locale.LC_TIME, "nl_NL")  # Dutch dates
        return self.start_date.strftime("%-d %B %Y")

    @property
    def end_date_string(self):
        locale.setlocale(locale.LC_TIME, "nl_NL")  # Dutch dates
        return self.end_date.strftime("%-d %B %Y")

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

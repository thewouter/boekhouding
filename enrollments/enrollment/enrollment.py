import json
import os
from datetime import datetime

from mollie.api.objects.payment_link import PaymentLink
from pydantic import BaseModel, ConfigDict

from enrollments.email import generate_enrollment_email, draft_email
from enrollments.mollie.generate_mollie_payment_link import generate_payment_link


class Enrollment(BaseModel):
    """A filled out enrollment form."""
    camp: str
    amount: float
    name: str
    end_date: datetime
    filename: str
    payment_link_cache: PaymentLink | None = None
    email: str

    model_config = ConfigDict(arbitrary_types_allowed=True) #  To prevent generating many payment links

    @classmethod
    def from_json(cls, json_data: dict, filename) -> "Enrollment":
        """Generate a new enrollment from JSON data and an uuid for traceability."""
        camp = json_data["activity"]["name"]
        price = json_data["activity"]["price"]
        names = [participant["name"] for participant in json_data["participants"]]
        year, month, day = json_data["activity"]["endDate"].split("-")
        end_date = datetime(year=int(year), month=int(month), day=int(day))
        email_address = json_data["participants"][0]["emailAddress"]
        if len(names) == 1:
            name = names[0]
        else:
            name = f"{', '.join(names[:-1])} en {names[-1]}"
        return cls(camp=camp, amount=price, name=name, end_date=end_date, filename=filename, email=email_address)

    @property
    def payment_link(self) -> PaymentLink:
        """Get the payment link for the Enrollment."""
        if self.payment_link_cache is None:
            self.payment_link_cache = generate_payment_link(self.name, self.camp, self.amount, self.end_date)
            if self.payment_link_cache is None:
                raise ValueError("Payment link not available")
        return self.payment_link_cache

    @property
    def json_representation(self) -> str:
        """Flatten the Enrollment to JSON."""
        return json.dumps({
            "camp": self.camp,
            "amount": f"{self.amount:0.2f}",
            "name": self.name,
            "payment_link": self.payment_link.payment_link,
            "email": self.email,
        })

    def write_to_file(self, folder: str) -> None:
        """Write the Enrollment object to a file for further processing."""
        with open(os.path.join(folder, self.filename), "w") as f:
            f.write(self.json_representation)

    def send_email_enrollment_confirmation(self) -> None:
        """Send a confirmation email to the (fist) enrollment participant."""
        html = generate_enrollment_email(
            name=self.name,
            camp=self.camp,
            payment_link=self.payment_link.payment_link,
            cost=self.amount
        )
        draft_email(
            mailbox="inschrijvingen@trapperskamp.com",  # info@ at a later time
            to_address=self.email,
            subject=f"Bevestiging inschrijving voor {self.camp}",
            body=html
        )



import os

from mollie.api.objects.payment_link import PaymentLink
from pydantic import BaseModel, ConfigDict

from traka_automation.enrollments.enrollment.camp import Camp
from traka_automation.enrollments.enrollment.participant import Participant
from traka_automation.enrollments.mollie_connection.generate_mollie_payment_link import (
    generate_payment_link,
)


class EnrollmentWebForm(BaseModel):
    """A filled out enrollment form."""

    camp: Camp
    participants: list[Participant] = []
    uuid: str
    payment_link_cache: PaymentLink | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  #  To prevent generating many payment links

    @classmethod
    def from_json(cls, json_data: dict, uuid) -> EnrollmentWebForm:
        """Generate a new enrollment from JSON data and an uuid for traceability."""
        camp_name = json_data["activity"]["name"]
        camp_price = json_data["activity"]["price"]
        camp_start_date = json_data["activity"]["startDate"]
        camp_end_date = json_data["activity"]["endDate"]
        camp = Camp(
            name=camp_name,
            price=camp_price,
            start_date=camp_start_date,
            end_date=camp_end_date,
        )
        uuid = uuid.split(".")[0]

        participants = json_data["participants"]
        participant_list = []
        for participant in participants:
            participant_list.append(Participant.from_json(participant, camp))

        return cls(camp=camp, participants=participant_list, uuid=uuid)

    @property
    def total_price(self):
        """The total price of the enrollment."""
        return sum([p.camp.price for p in self.participants])

    @property
    def combined_names(self):
        """The combined names of the enrollment participants."""
        names = [participant.name for participant in self.participants]
        if len(names) == 1:
            combined_names = names[0]
        else:
            combined_names = f"{', '.join(names[:-1])} en {names[-1]}"
        return combined_names

    @property
    def payment_link(self) -> PaymentLink:
        """Get the payment link for the Enrollment."""
        if self.payment_link_cache is None:
            self.payment_link_cache = generate_payment_link(
                self.combined_names,
                self.camp.name,
                self.total_price,
                self.camp.end_date,
            )
            if self.payment_link_cache is None:
                raise ValueError("Payment link not available")
        return self.payment_link_cache

    @property
    def json_representation(self) -> str:
        """Flatten the Enrollment to JSON."""
        return self.model_dump_json()

    @property
    def email_addresses(self) -> list[str]:
        return [p.email_address for p in self.participants]

    def write_to_file(self, folder: str) -> None:
        """Write the Enrollment object to a file for further processing."""
        filename = os.path.join(folder, f"{self.uuid}.json")
        with open(filename, "w") as f:
            f.write(self.json_representation)

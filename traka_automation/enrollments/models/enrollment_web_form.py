from pydantic import BaseModel, ConfigDict

from traka_automation.enrollments.models.camp import Camp
from traka_automation.enrollments.models.participant import Participant
from traka_automation.enrollments.models.payment_link import TrakaPaymentLink


class EnrollmentWebForm(BaseModel):
    """A filled out enrollment form."""

    camp: Camp
    participants: list[Participant] = []
    uuid: str
    payment_link_cache: TrakaPaymentLink | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_json(cls, json_data: dict, uuid) -> EnrollmentWebForm:
        """Generate a new enrollment from JSON data and an uuid for traceability."""
        camp_name = json_data["activity"]["name"]
        camp_price = json_data["activity"].get("price")
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
        return sum(
            [p.camp.price for p in self.participants if p.camp.price is not None]
        )

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
    def json_representation(self) -> str:
        """Flatten the Enrollment to JSON."""
        return self.model_dump_json()

    @property
    def email_addresses(self) -> list[str]:
        return [p.email_address for p in self.participants]

    @property
    def has_payment_info(self):
        """Whether this enrollment requires a payment link."""
        return self.camp.price is not None

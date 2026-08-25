from datetime import date

from datauri import DataURI
from pydantic import BaseModel

from traka_automation.enrollments.models import Camp


no_photo = DataURI.from_file("traka_automation/enrollments/templates/no_photo.png")

class Participant(BaseModel):
    """A participant of a camp."""

    # camp
    camp: Camp

    # personal details
    name: str
    zip_code: str
    address: str
    city: str
    birth_date: date
    email_address: str
    phone: str
    dietary_restrictions: str
    photo: DataURI
    backup_name: str
    backup_email_address: str
    backup_phone: str

    # Scouting membership
    member_number: str
    scouting_group: str
    scouting_city: str
    age_group: str

    @classmethod
    def from_json(cls, json_data, camp):
        """Load a participant from a JSON data dictionary."""
        name = json_data["name"]
        zip_code = json_data["zipCode"]
        city = json_data["city"]
        address = json_data["address"]
        birth_date = date.fromisoformat(json_data["birthDate"])
        email_address = json_data["emailAddress"]
        phone = json_data["telephone"]
        dietary_restrictions = json_data["dietaryRestrictions"]

        photo = json_data.get("photo", no_photo)
        backup_name = json_data["iceName"]
        backup_email_address = json_data.get("iceEmailAddress", "")
        backup_phone = json_data["icePhone"]

        member_number = json_data["membership"].get("memberId", "")
        scouting_group = json_data["membership"]["group"]["name"]
        scouting_city = json_data["membership"]["group"]["city"]
        age_group = json_data["membership"].get("ageGroup", "")

        return cls(
            camp=camp,
            name=name,
            zip_code=zip_code,
            city=city,
            address=address,
            birth_date=birth_date,
            email_address=email_address,
            phone=phone,
            dietary_restrictions=dietary_restrictions,
            photo=photo,
            backup_name=backup_name,
            backup_email_address=backup_email_address,
            backup_phone=backup_phone,
            member_number=member_number,
            scouting_group=scouting_group,
            scouting_city=scouting_city,
            age_group=age_group,
        )

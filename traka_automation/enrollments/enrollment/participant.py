from pydantic import BaseModel

from traka_automation.enrollments.enrollment.camp import Camp


class Participant(BaseModel):
    """A participant of a camp."""
    #camp
    camp: Camp

    # personal details
    name: str
    zip_code: str
    address: str
    city: str
    birth_date: str
    email_address: str
    phone: str
    backup_email_address: str
    backup_phone: str

    # Scouting membership
    member_number: str
    scouting_group: str
    scouting_city: str
    age_group: str

    @classmethod
    def from_json(cls, json_data, camp):
        camp = camp

        name = json_data["name"]
        zip_code = json_data["zipCode"]
        city = json_data["city"]
        address = json_data["address"]
        birth_date = json_data["birthDate"]
        email_address = json_data["emailAddress"]
        phone = json_data["telephoneMobile"]
        backup_email_address = json_data["backupEmailAddress"]
        backup_phone = json_data["backupPhone"]

        member_number = json_data["membership"]["memberId"]
        scouting_group = json_data["membership"]["group"]["name"]
        scouting_city = json_data["membership"]["group"]["city"]
        age_group = json_data["membership"]["ageGroup"]

        return cls(
            camp=camp,
            name=name,
            zip_code=zip_code,
            city=city,
            address=address,
            birth_date=birth_date,
            email_address=email_address,
            phone=phone,
            backup_email_address=backup_email_address,
            backup_phone=backup_phone,
            member_number=member_number,
            scouting_group=scouting_group,
            scouting_city=scouting_city,
            age_group=age_group
        )
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from traka_automation.enrollments.models import (
    EnrollmentWebForm,
)
from traka_automation.util.config import secrets_config


def generate_enrollment_email(enrollment_form: EnrollmentWebForm) -> str:
    """Generate an enrollment email_handler in HTML."""
    env = Environment(
        loader=FileSystemLoader(Path(__file__).resolve().parent.parent / "templates"),
        autoescape=True,
    )

    if enrollment_form.has_payment_info:
        template = env.get_template("enrollment_confirmation.html")
        html = template.render(
            participant_names=enrollment_form.combined_names,
            camp_name=enrollment_form.camp.name,
            payment_url=enrollment_form.payment_link.payment_link,  # type: ignore
            amount=enrollment_form.total_price,
            signature_name=secrets_config["email"]["signature_name"],
            signature_title=secrets_config["email"]["signature_title"],
            logo_url="https://next.trapperskamp.com/processed_images/trapperskamp-vught.a83be22bfa0f671b.webp",
            camp_start_date=enrollment_form.camp.start_date_string,
            camp_end_date=enrollment_form.camp.end_date_string,
        )
    else:
        template = env.get_template("enrollment_confirmation_no_payment.html")
        html = template.render(
            participant_names=enrollment_form.combined_names,
            camp_name=enrollment_form.camp.name,
            signature_name=secrets_config["email"]["signature_name"],
            signature_title=secrets_config["email"]["signature_title"],
            logo_url="https://next.trapperskamp.com/processed_images/trapperskamp-vught.a83be22bfa0f671b.webp",
            camp_start_date=enrollment_form.camp.start_date_string,
            camp_end_date=enrollment_form.camp.end_date_string,
        )

    return html

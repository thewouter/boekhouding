from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from traka_automation.enrollments.enrollment.enrollment_web_form import (
    EnrollmentWebForm,
)


def generate_enrollment_email(enrollment_form: EnrollmentWebForm) -> str:
    """Generate an enrollment email_handler in HTML."""
    env = Environment(
        loader=FileSystemLoader(Path(__file__).resolve().parent.parent / "templates"),
        autoescape=True,
    )

    template = env.get_template("enrollment_confirmation.html")
    html = template.render(
        participant_names=enrollment_form.combined_names,
        camp_name=enrollment_form.camp.name,
        payment_url=enrollment_form.payment_link.payment_link,
        amount=enrollment_form.total_price,
        signature_name="Wouter van Harten",
        signature_title="Penningmeester Plusscoutskring Trapperskamp",
        logo_url="https://next.trapperskamp.com/processed_images/trapperskamp-vught.a83be22bfa0f671b.webp",
        camp_start_date=enrollment_form.camp.start_date_string,
        camp_end_date=enrollment_form.camp.end_date_string,
    )

    return html

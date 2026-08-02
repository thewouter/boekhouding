import subprocess
from pathlib import Path

from docxtpl import DocxTemplate

from traka_automation.enrollments.enrollment.participant import Participant
from traka_automation.util.dutch_date import dutch_date


def generate_docx_enrollment_form(participant: Participant) -> DocxTemplate:
    """Generate an enrollment form."""
    doc = DocxTemplate(
        f"{Path(__file__).resolve().parent.parent}/templates/aanmeldformulier.docx"
    )

    context = {
        "camp": {
            "name": participant.camp.name,
            "year": participant.camp.start_date.year,
            "text_date_start": participant.camp.start_date_string,
            "text_date_end": participant.camp.end_date_string,
        },
        "participant": {
            "name": participant.name,
            "address": participant.address,
            "city": participant.city,
            "birth_date": dutch_date(participant.birth_date),
            "email_address": participant.email_address,
            "phone": participant.phone,
            "backup_email_address": participant.backup_email_address,
            "backup_phone": participant.backup_phone,
            "member_number": participant.member_number,
            "scouting_group": participant.scouting_group,
            "scouting_city": participant.scouting_city,
            "age_group": participant.age_group,
        },
        "payment_term": {
            "one": {
                "text": participant.camp.cancellation_term_one.text_date,
                "retainer": participant.camp.cancellation_term_one.retainer,
            },
            "two": {
                "text": participant.camp.cancellation_term_two.text_date,
                "retainer": participant.camp.cancellation_term_two.retainer,
            },
        },
    }

    doc.render(context)

    return doc


def save_enrollment_form(enrollment_form: DocxTemplate, filename: str) -> None:
    """Save the enrollment form to the given filename."""
    enrollment_form.save(filename=filename)


def convert_docx_to_pdf(docx_path: str) -> None:
    """Convert the given docx file to PDF."""
    print(str(Path(docx_path).parent))
    subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            str(docx_path),
            "--outdir",
            str(Path(docx_path).parent),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def generate_enrollment_form_and_save(filename, participant: Participant) -> None:
    """Generate an enrollment form and save it to the given filename as docx and PDF."""
    enrollment_form = generate_docx_enrollment_form(participant)
    save_enrollment_form(enrollment_form, filename)
    convert_docx_to_pdf(filename)

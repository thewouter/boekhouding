import subprocess
from io import BytesIO
from pathlib import Path

from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from traka_automation.enrollments.models import Participant
from traka_automation.util.dutch_date import dutch_date


def _get_payment_texts(participant: Participant) -> tuple[str, str, str, str]:
    if participant.camp.price is not None:
        price = f" € {participant.camp.price:0.2f}"
        price_text = "van"
        retainer_one_price = participant.camp.cancellation_term_one.text_retainer
        retainer_two_price = participant.camp.cancellation_term_two.text_retainer
    else:
        price = ""
        price_text = "dat later gecommuniceerd gaat worden"
        retainer_one_price = "een kwart van het deelnemersgeld"
        retainer_two_price = "de helft van het deelnemersgeld"
    return price, price_text, retainer_one_price, retainer_two_price


def _get_photo_data(doc: DocxTemplate, participant: Participant) -> InlineImage:
    return InlineImage(doc, BytesIO(participant.photo.data), width=Mm(35))


def generate_docx_enrollment_form(participant: Participant) -> DocxTemplate:
    """Generate an enrollment form."""
    doc = DocxTemplate(
        f"{Path(__file__).resolve().parent.parent}/templates/aanmeldformulier.docx"
    )

    photo_image = _get_photo_data(doc, participant)
    price, price_text, retainer_one_price, retainer_two_price = _get_payment_texts(
        participant
    )

    context = {
        "camp": {
            "name": participant.camp.name,
            "year": participant.camp.start_date.year,
            "text_date_start": participant.camp.start_date_string,
            "text_date_end": participant.camp.end_date_string,
            "price": price,
            "price_text": price_text,
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
            "backup_name": participant.backup_name,
            "member_number": participant.member_number,
            "scouting_group": participant.scouting_group,
            "scouting_city": participant.scouting_city,
            "age_group": participant.age_group,
            "dietary_restrictions": participant.dietary_restrictions,
            "photo": photo_image,
        },
        "cancellation_term": {
            "one": {
                "text": participant.camp.cancellation_term_one.text_date,
                "retainer": retainer_one_price,
            },
            "two": {
                "text": participant.camp.cancellation_term_two.text_date,
                "retainer": retainer_two_price,
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


def generate_enrollment_form_and_save(filename, participant: Participant) -> Path:
    """Generate an enrollment form and save it to the given filename as docx and PDF."""
    enrollment_form = generate_docx_enrollment_form(participant)
    save_enrollment_form(enrollment_form, filename)
    convert_docx_to_pdf(filename)
    return Path(filename).with_suffix(".pdf")

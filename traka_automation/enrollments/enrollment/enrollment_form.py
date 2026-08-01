import subprocess
from pathlib import Path

from docxtpl import DocxTemplate

def generate_docx_enrollment_form() -> DocxTemplate:
    """Generate an enrollment form."""
    doc = DocxTemplate(f"{Path(__file__).resolve().parent.parent}/templates/aanmeldformulier.docx")

    context = {
        "camp": {
            "name": "Jungle Adventure",
            "year": 2020,
            "text_date_start": "2 january 2020",
            "text_date_end": "2 february 2020",
        },
        "participant": {
            "name": "Jan Jansen",
            "address": "6548 DE",
            "city": "Amsterdkam",
            "birth_date": "1980-01-19",
            "email_address": "testmai@adres.com",
            "phone": "0612345678",
            "backup_email_address": "papaenmama@amil.com",
            "backup_phone": "0612345678",
            "member_number": "665546",
            "scouting_group": "Scouting naampe",
            "scouting_city": "Amsterdkam",
            "age_group": "Bevers",
        },
        "payment_term": {
            "one": {
                "text": "30 november 2019",
                "retainer": "50,00"
            },
            "two": {
                "text": "40 november 2019",
                "retainer": "80,00"
            }
        }
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
            "--convert-to", "pdf",
            str(docx_path),
            "--outdir",
            str(Path(docx_path).parent),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

def generate_enrollment_form_and_save(filename) -> None:
    """Generate an enrollment form and save it to the given filename as docx and PDF."""
    enrollment_form = generate_docx_enrollment_form()
    save_enrollment_form(enrollment_form, filename)
    convert_docx_to_pdf(filename)
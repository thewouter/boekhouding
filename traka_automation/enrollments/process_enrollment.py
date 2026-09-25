import os
from pathlib import Path

from traka_automation.enrollments.email_handler import (
    draft_email,
    generate_enrollment_email,
)
from traka_automation.enrollments.enrollment.enrollment_form import (
    generate_enrollment_form_and_save,
)
from traka_automation.enrollments.models import (
    EnrollmentWebForm,
)
from traka_automation.settings import get_settings
from traka_automation.util.json import load_json, write_json

OUTPUT_FOLDER = "/onedrive/data/exchange_folder/inschrijfformulieren"


def send_email_enrollment_confirmation(
    enrollment_web_form: EnrollmentWebForm, forms: list[Path] | None = None
) -> None:
    """Send a confirmation email_handler to the (fist) enrollment participant."""
    if forms is None:
        forms = []
    attachments = forms.copy()
    if enrollment_web_form.has_adult_participant:
        attachments.append(
            Path(__file__).resolve().parent / "templates" / "Gezondheidsformulier_18+.pdf"
        )
    if enrollment_web_form.has_minor_participant:
        attachments.append(
            Path(__file__).resolve().parent / "templates" / "Gezondheidsformulier_18-.pdf"
        )
    settings = get_settings()
    html = generate_enrollment_email(enrollment_web_form, settings)
    if settings.dev:
        return
    draft_email(
        mailbox=settings.email.mailbox,
        to_addresses=enrollment_web_form.email_addresses,
        subject=f"Bevestiging inschrijving voor {enrollment_web_form.camp.name} {enrollment_web_form.camp.year}",
        body=html,
        attachments=attachments,
        settings=settings.ms_graph,
    )


def generate_and_save_enrollment_forms(
    enrollment_web_form: EnrollmentWebForm, folder: str
) -> list[Path]:
    """Generate an enrollment form and save it to the given folder for all participants."""
    paths: list[Path] = []
    for participant in enrollment_web_form.participants:
        participant_name_camp_name = f"{participant.name.replace(' ', '_')}_{participant.camp.name.replace(' ', '_')}"
        participant_folder = f"{folder}/{participant_name_camp_name}"
        os.makedirs(participant_folder, exist_ok=True)
        filename = f"{participant_folder}/{participant_name_camp_name}.docx"
        path = generate_enrollment_form_and_save(filename, participant)
        paths.append(path)

        write_json(
            data=participant.json_for_excel_overview,
            path=f"{participant_folder}/data.json",
        )
    return paths


def load_new_enrollments() -> list[EnrollmentWebForm]:
    """Load all new enrollments into a list."""
    new_enrollments: list[EnrollmentWebForm] = []
    directory = "/onedrive/data/exchange_folder/inschrijvingen"
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            data = load_json(os.path.join(directory, filename))
            new_enrollments.append(EnrollmentWebForm.from_json(data, filename))
    return new_enrollments


def process_enrollment(enrollment: EnrollmentWebForm) -> None:
    """Process the enrollment and save the generated files to the given folder for all participants."""
    print(f"processing enrollment {enrollment}")
    pdf_files = generate_and_save_enrollment_forms(enrollment, folder=OUTPUT_FOLDER)
    send_email_enrollment_confirmation(enrollment, pdf_files)
    # os.remove(f"/onedrive/data/exchange_folder/inschrijvingen/{enrollment.uuid}.json")


def main():
    """Main enrollment loop."""
    new_enrollments = load_new_enrollments()
    for enrollment in new_enrollments:
        process_enrollment(enrollment)


if __name__ == "__main__":
    main()

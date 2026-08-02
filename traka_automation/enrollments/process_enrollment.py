import os

from traka_automation.enrollments.email_handler import (
    generate_enrollment_email,
    draft_email,
)
from traka_automation.enrollments.enrollment.enrollment_web_form import (
    EnrollmentWebForm,
)
from traka_automation.enrollments.enrollment.enrollment_form import (
    generate_enrollment_form_and_save,
)
from traka_automation.util.load_json import load_json


OUTPUT_FOLDER = "/onedrive/data/exchange_folder/inschrijfformulieren"


def send_email_enrollment_confirmation(enrollment_web_form: EnrollmentWebForm) -> None:
    """Send a confirmation email_handler to the (fist) enrollment participant."""
    html = generate_enrollment_email(enrollment_web_form)
    draft_email(
        mailbox="inschrijvingen@trapperskamp.com",  # info@ at a later time
        to_addresses=enrollment_web_form.email_addresses,
        subject=f"Bevestiging inschrijving voor {enrollment_web_form.camp.name} {enrollment_web_form.camp.year}",
        body=html,
    )


def generate_and_save_enrollment_forms(
    enrollment_web_form: EnrollmentWebForm, folder: str
) -> None:
    """Generate an enrollment form and save it to the given folder for all participants."""
    for participant in enrollment_web_form.participants:
        filename = f"{folder}/{participant.name.replace(' ', '_')}.docx"
        generate_enrollment_form_and_save(filename, participant)


def load_new_enrollments():
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
    enrollment.write_to_file(folder=OUTPUT_FOLDER)
    send_email_enrollment_confirmation(enrollment)
    generate_and_save_enrollment_forms(enrollment, folder=OUTPUT_FOLDER)
    # os.remove(f"/onedrive/data/exchange_folder/inschrijvingen/{enrollment.filename}")


def main():
    """Main enrollment loop."""
    new_enrollments = load_new_enrollments()
    for enrollment in new_enrollments:
        process_enrollment(enrollment)


if __name__ == "__main__":
    main()

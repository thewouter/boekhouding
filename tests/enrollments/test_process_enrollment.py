from pathlib import Path

from traka_automation.enrollments.enrollment.enrollment_web_form import (
    EnrollmentWebForm,
)
from traka_automation.enrollments.process_enrollment import (
    generate_and_save_enrollment_forms,
    send_email_enrollment_confirmation,
)


def test_send_email_enrollment_confirmation(
    example_enrollment_web_form: EnrollmentWebForm,
):
    send_email_enrollment_confirmation(example_enrollment_web_form)


def test_generate_and_save_enrollment_forms(
    example_enrollment_web_form: EnrollmentWebForm, tmp_path: Path
):
    generate_and_save_enrollment_forms(example_enrollment_web_form, str(tmp_path))
    counter = 0
    for file in tmp_path.iterdir():
        assert file.is_file()
        counter += 1
    assert counter == len(example_enrollment_web_form.participants) * 2

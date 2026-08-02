import hashlib
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
    hashes = []
    for file in tmp_path.iterdir():
        assert file.is_file()
        hashes.append(hashlib.md5(file.read_bytes()).hexdigest())
    assert hashes == [
        "edfbcc184c0cb3ba8e52f86ad611809e",
        "318963ca8d16f5ccf28086447a265e72",
        "9489087374ca2701a707541847be0fa1",
        "3759822c27586ac1a8ab255d6df37277",
    ]

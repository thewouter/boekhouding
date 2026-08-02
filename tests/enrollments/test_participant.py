from traka_automation.enrollments.enrollment.enrollment_web_form import (
    EnrollmentWebForm,
)


def test_enrollment_from_json(enrollment_json):
    enrollment = EnrollmentWebForm.from_json(enrollment_json, uuid="test-uuid")
    assert isinstance(enrollment, EnrollmentWebForm)

import html5lib

from traka_automation.enrollments.email_handler import generate_enrollment_email
from traka_automation.enrollments.enrollment.enrollment_web_form import (
    EnrollmentWebForm,
)


def test_enrollment_email(example_enrollment_web_form: EnrollmentWebForm):
    """Test whether the enrollment email generation generates valid HTML5."""
    html = generate_enrollment_email(example_enrollment_web_form)
    html5parser = html5lib.HTMLParser(strict=True)
    html5parser.parse(html)


def test_enroll_email_content_keywords(example_enrollment_web_form: EnrollmentWebForm):
    html = generate_enrollment_email(example_enrollment_web_form)
    assert example_enrollment_web_form.camp.start_date_string in html
    assert example_enrollment_web_form.camp.end_date_string in html
    assert example_enrollment_web_form.camp.name in html
    for participant in example_enrollment_web_form.participants:
        assert participant.name in html
    assert f"{example_enrollment_web_form.total_price:0.2f}" in html
    assert example_enrollment_web_form.payment_link.payment_link in html
    assert example_enrollment_web_form.combined_names in html

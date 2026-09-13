import html5lib

from traka_automation.enrollments.email_handler import generate_enrollment_email
from traka_automation.enrollments.models import (
    EnrollmentWebForm,
)
from traka_automation.enrollments.payment_connection import get_payment_link
from traka_automation.settings import get_settings


def test_enrollment_email(example_enrollment_web_form: EnrollmentWebForm):
    """Test whether the enrollment email generation generates valid HTML5."""
    settings = get_settings()
    html = generate_enrollment_email(
        example_enrollment_web_form,
        settings,
    )
    html5parser = html5lib.HTMLParser(strict=True)
    html5parser.parse(html)


def test_enrollment_email_no(example_enrollment_web_form_no_price: EnrollmentWebForm):
    """Test whether the enrollment email generation generates valid HTML5."""
    settings = get_settings()
    html = generate_enrollment_email(
        example_enrollment_web_form_no_price,
        settings,
    )
    html5parser = html5lib.HTMLParser(strict=True)
    html5parser.parse(html)


def test_enroll_email_content_keywords(example_enrollment_web_form: EnrollmentWebForm):
    """Test whether the enrollment email generation contains the expected keywords."""
    settings = get_settings()
    html = generate_enrollment_email(example_enrollment_web_form, settings)
    assert example_enrollment_web_form.camp.start_date_string in html
    assert example_enrollment_web_form.camp.end_date_string in html
    assert example_enrollment_web_form.camp.name in html
    for participant in example_enrollment_web_form.participants:
        assert participant.name in html
    assert f"{example_enrollment_web_form.total_price:0.2f}" in html
    assert get_payment_link(example_enrollment_web_form, settings).payment_link in html  # type: ignore
    assert example_enrollment_web_form.combined_names in html


def test_enroll_email_content_keywords_no_price(
    example_enrollment_web_form_no_price: EnrollmentWebForm,
):
    """Test whether the enrollment email generation contains the expected keywords."""
    settings = get_settings()
    html = generate_enrollment_email(example_enrollment_web_form_no_price, settings)
    assert example_enrollment_web_form_no_price.camp.start_date_string in html
    assert example_enrollment_web_form_no_price.camp.end_date_string in html
    assert example_enrollment_web_form_no_price.camp.name in html
    for participant in example_enrollment_web_form_no_price.participants:
        assert participant.name in html
    assert example_enrollment_web_form_no_price.combined_names in html
    assert "€" not in html
    assert "betaal" not in html

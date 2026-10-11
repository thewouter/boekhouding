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


def test_enrollment_email_single_term_does_not_mention_terms(
    example_enrollment_web_form: EnrollmentWebForm,
):
    """Test that camps without two payment terms only show the single payment option."""
    settings = get_settings()
    html = generate_enrollment_email(example_enrollment_web_form, settings)
    assert "twee termijnen" not in html
    assert "Vóór" not in html


def test_enrollment_email_two_terms_is_valid_html(
    example_enrollment_web_form_two_terms: EnrollmentWebForm,
):
    """Test whether the enrollment email generation generates valid HTML5."""
    settings = get_settings()
    html = generate_enrollment_email(example_enrollment_web_form_two_terms, settings)
    html5parser = html5lib.HTMLParser(strict=True)
    html5parser.parse(html)


def test_enrollment_email_two_terms_content(
    example_enrollment_web_form_two_terms: EnrollmentWebForm,
):
    """Test that camps allowing two payment terms show both terms with their amounts and due date."""
    settings = get_settings()
    camp = example_enrollment_web_form_two_terms.camp
    html = generate_enrollment_email(example_enrollment_web_form_two_terms, settings)
    assert "twee termijnen" in html
    assert f"{camp.payment_term_one:.2f}" in html
    assert f"{camp.payment_term_two:.2f}" in html
    assert camp.cancellation_term_one.text_date in html
    assert "Mocht je dit liever direct overmaken, dan kan dat ook." not in html

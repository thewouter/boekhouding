from traka_automation.enrollments.models import (
    EnrollmentWebForm,
    TrakaPaymentLink,
)
from traka_automation.enrollments.payment_connection import get_payment_link
from traka_automation.settings import get_settings


def test_enrollment_from_json(example_enrollment_json):
    enrollment = EnrollmentWebForm.from_json(example_enrollment_json, uuid="test-uuid")
    assert isinstance(enrollment, EnrollmentWebForm)

    assert len(enrollment.participants) == 2


def test_enrollment_form_no_price(
    example_enrollment_web_form_no_price: EnrollmentWebForm,
):
    assert isinstance(example_enrollment_web_form_no_price, EnrollmentWebForm)
    assert example_enrollment_web_form_no_price.total_price == 0.0


def test_get_payment_link(example_enrollment_web_form: EnrollmentWebForm):
    payment_link = get_payment_link(example_enrollment_web_form, get_settings())
    assert isinstance(payment_link, TrakaPaymentLink)
    assert payment_link.payment_link == "https://google.com"


def test_get_payment_link_cache(example_enrollment_web_form: EnrollmentWebForm):
    # Ensure the payment link cache is initially None
    assert example_enrollment_web_form.payment_link_cache is None

    # Generate the payment link and check if it is cached
    payment_link = get_payment_link(example_enrollment_web_form, get_settings())
    assert isinstance(payment_link, TrakaPaymentLink)
    assert example_enrollment_web_form.payment_link_cache is not None
    assert example_enrollment_web_form.payment_link_cache == payment_link


def test_enrollment_web_form_properties_no_price(
    example_enrollment_web_form_no_price: EnrollmentWebForm,
):
    assert example_enrollment_web_form_no_price.total_price == 0.0
    assert example_enrollment_web_form_no_price.combined_names == "Jan Jansen"
    assert example_enrollment_web_form_no_price.payment_link_cache is None
    get_payment_link(example_enrollment_web_form_no_price, get_settings())
    assert example_enrollment_web_form_no_price.payment_link_cache is None
    assert not example_enrollment_web_form_no_price.has_payment_info


def test_enrollment_web_form_properties(example_enrollment_web_form: EnrollmentWebForm):
    assert example_enrollment_web_form.total_price == 175.5 + 175.5
    assert example_enrollment_web_form.combined_names == "Jan Jansen en Piet Jansen"
    assert example_enrollment_web_form.payment_link_cache is None
    get_payment_link(example_enrollment_web_form, get_settings())
    assert isinstance(example_enrollment_web_form.payment_link_cache, TrakaPaymentLink)
    assert example_enrollment_web_form.json_representation.startswith(
        '{"camp":{"name":"Jungle '
        'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"participants":[{"camp":{"name":"Jungle '
        'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Jan '
        'Jansen","zip_code":"1234 AB","address":"Voorbeeldstraat '
        '1","city":"Voorbeeldstad","birth_date":"2016-03-15","email_address":"wouter@woutervanharten.nl","phone":"06-12345678","dietary_restrictions":"Ik '
        "mag geen rijst op "
    )
    assert example_enrollment_web_form.email_addresses == [
        "wouter@woutervanharten.nl",
        "wouter.van.harten@trapperskamp.com",
    ]


def test_enrollment_web_form_to_json(example_enrollment_web_form: EnrollmentWebForm):
    json_representation = example_enrollment_web_form.json_representation
    assert isinstance(json_representation, str)
    assert json_representation.startswith(
        '{"camp":{"name":"Jungle '
        'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"participants":[{"camp":{"name":"Jungle '
        'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Jan '
        'Jansen","zip_code":"1234 AB","address":"Voorbeeldstraat '
        '1","city":"Voorbeeldstad","birth_date":"2016-03-15","email_address":"wouter@woutervanharten.nl","phone":"06-12345678","dietary_restrictions":"Ik '
        "mag geen rijst op "
        'woensdagen","photo":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAACXBIWXMAAAsSAAALEgHS3X78AAAARElEQVQIHWM8zRn3/wb7U4aoDzYMTAyMDIwHuMP/7+K5zPCb6Q/DP4b/DCx6P+QY7rO9Ykh4bw8WYPzP0PAfJANSDgIAgkYYUh06X6cAAAAASUVORK5CYII==","backup_name":"Papa '
    )


def test_has_minor_and_adult_participants(
    example_enrollment_web_form: EnrollmentWebForm,
):
    """Test the has_minor_participant and has_adult_participant properties of EnrollmentWebForm."""
    assert example_enrollment_web_form.has_minor_participant is True
    assert example_enrollment_web_form.has_adult_participant is True

    adult = example_enrollment_web_form.participants[1]
    del example_enrollment_web_form.participants[1]
    assert example_enrollment_web_form.has_minor_participant is True
    assert example_enrollment_web_form.has_adult_participant is False
    example_enrollment_web_form.participants.append(adult)
    del example_enrollment_web_form.participants[0]
    assert example_enrollment_web_form.has_minor_participant is False
    assert example_enrollment_web_form.has_adult_participant is True
